import time
import subprocess
import signal
import threading
import os
from pathlib import Path
from gi.repository import GLib, Gtk

from ..engine import build_ffmpeg_command, ProgressParser
from ..utils import ui, SleepInhibitor
from ..config import (
    AUTO_CLOSE_MAP,
    CODECS,
    GPU_BITRATE_TARGETS,
    GPU_QV_MAP_AV1,
    GPU_QV_MAP_HEVC,
    QUALITY_MAP_GPU,
    QUALITY_MAP_CPU,
    DEFAULT_COMPRESSION_LEVEL,
    OUTPUT_DIR_NAME,
)
from .. import utils

class ConversionManager:
    def __init__(self, window):
        self.window = window
        self.stop_requested = False
        self.paused = False
        self.ffmpeg_process = None
        self.current_file_row = None
        self.sleep_inhibitor = SleepInhibitor()
        self.queue_status = window.queue_status # Reference to label

    def start_encoding(self):
        self.stop_requested = False
        self.paused = False
        self.window.start_btn.set_visible(False)
        self.window.stop_btn.set_visible(True)
        self.window.stop_btn.set_sensitive(True)
        self.window.pause_btn.set_visible(True)
        self.window.pause_btn.set_sensitive(True)
        self.window.add_btn.set_sensitive(True)
        self.window.open_out_btn.set_sensitive(False)

        self.sleep_inhibitor.start()

        # Start Thread
        t = threading.Thread(target=self._run_queue, daemon=True)
        t.start()

    def stop_encoding(self):
        self.stop_requested = True
        self.current_file_row = None
        if self.ffmpeg_process:
            try:
                self.ffmpeg_process.terminate()
                # Give it a moment, then force kill if still running
                try:
                    self.ffmpeg_process.wait(timeout=0.5)
                except:
                    self.ffmpeg_process.kill()  # Force kill
            except:
                pass
            self.ffmpeg_process = None

        self.window.stop_btn.set_sensitive(False)
        self.window.pause_btn.set_sensitive(False)
        self.queue_status.set_text("Stopped")

        # Cancel any running countdown (auto-close/shutdown)
        self.window.cancel_countdown()

        # Re-enable buttons
        self.window.start_btn.set_visible(True)
        self.window.stop_btn.set_visible(False)
        self.window.pause_btn.set_visible(False)
        self.window.add_btn.set_sensitive(True)

        # Re-enable row remove buttons
        for row in self.window.file_manager.files.values():
            row.remove_btn.set_sensitive(True)

    def pause_resume(self):
        self.paused = not self.paused
        if self.paused:
            if self.ffmpeg_process:
                os.kill(self.ffmpeg_process.pid, signal.SIGSTOP)
            self.window.pause_btn.set_image(Gtk.Image.new_from_icon_name("media-playback-start-symbolic", Gtk.IconSize.BUTTON))
            self.queue_status.set_text("Paused")
        else:
            if self.ffmpeg_process:
                os.kill(self.ffmpeg_process.pid, signal.SIGCONT)
            self.window.pause_btn.set_image(Gtk.Image.new_from_icon_name("media-playback-pause-symbolic", Gtk.IconSize.BUTTON))
            self.queue_status.set_text("Processing...")

    def _run_queue(self):
        while not self.stop_requested:
            file_list = self.window.file_manager.get_file_list()
            
            # Find the first pending file
            row = None
            current_index = -1
            for i, r in enumerate(file_list):
                if r.status == "pending":
                    row = r
                    current_index = i
                    break
            
            if row is None:
                # No more pending files
                break

            total = len(file_list)
            self.current_file_row = row
            path = row.path

            ui(row.set_active, True)
            ui(row.set_reorder_locked, True)
            ui(row.remove_btn.set_sensitive, False)
            ui(self.queue_status.set_text, f"Processing {current_index + 1} of {total}...")

            ui(setattr, row, "status", "processing")
            result = self._encode_file(row, current_index)

            ui(row.set_active, False)
            ui(row.set_reorder_locked, False)
            ui(row.remove_btn.set_sensitive, True)
            
            if result is not None:
                elapsed, init_size, init_size_str = result
                ui(row.set_success)
                from .. import utils
                final_size = utils.get_file_size(row.out_path)
                final_size_str = utils.human_readable_size(final_size)
                
                # Calculate compression percentage
                diff = init_size - final_size
                compression_pct = (diff / init_size * 100) if init_size > 0 else 0
                
                ui(row.set_finished, elapsed, init_size_str, final_size_str, compression_pct)
                ui(row.play_btn.set_visible, True)
            else:
                # If it failed or was stopped, it shouldn't be "pending" anymore if we want to skip it, 
                # but if stopped we might want to resume. 
                # For now, if result is None and not stop_requested, mark as error.
                if not self.stop_requested:
                    ui(row.set_error, "Encoding Failed")

        self.sleep_inhibitor.stop()
        ui(self._on_queue_finished)

    def _encode_file(self, row, current_index):
        # Resolve parameters from row.params
        p = row.params
        codec_key = p.get("codec_key", "HEVC (VAAPI 10-bit)")
        params = {
            "codec": CODECS.get(codec_key, CODECS["HEVC (VAAPI 10-bit)"]),
            "gpu": p.get("gpu", "cpu"),
            "scale": p.get("scale", True),
            "compression_level": p.get("compression_level", DEFAULT_COMPRESSION_LEVEL)
        }
        
        # Resolve quality preset from UI
        q_label_full = p.get("quality_text", "Main - 65%")
        q_map = QUALITY_MAP_CPU if "CPU" in codec_key else QUALITY_MAP_GPU
        q_level = q_map.get(q_label_full, "main" if "CPU" not in codec_key else 6)

        # Get video info (duration, fps, codec, total_bitrate, video_bitrate, width)
        res = utils.get_video_info(row.path)
        duration, fps, input_codec, total_bitrate, video_bitrate, width = res

        # Calculate target for VIDEO stream only (bits/s)
        if "CPU" in codec_key:
            params["quality"] = q_level
            multiplier = 0.65 # Fallback for CPU
        else:
            # GPU Specific targeting
            is_hevc = "HEVC" in codec_key
            qv_map = GPU_QV_MAP_HEVC if is_hevc else GPU_QV_MAP_AV1
            # We use the calibrated QV number for the encoder
            params["quality"] = qv_map.get(q_level, 26 if not is_hevc else 21)
            # We use the standard multiplier for the bitrate target
            multiplier = GPU_BITRATE_TARGETS.get(q_level, 0.65)
        
        # We target a percentage of the VIDEO bitrate
        target_bitrate = int(video_bitrate * multiplier)
        
        # Peak cap: Don't let the video peak go much higher than the original video.
        max_bitrate = min(int(target_bitrate * 2.5), int(video_bitrate * 1.1))
        
        # Absolute floors (prevent total failure on weird files)
        target_bitrate = max(target_bitrate, 500_000)
        max_bitrate = max(max_bitrate, 1_000_000)

        # Prepare output path and parameters
        codec_settings = row.params.get("codec_key", "HEVC (VAAPI 10-bit)")
        q_label = row.params.get("quality_text", "Main - 65% (QV-26)")
        mode_label = row.params.get("process_mode", "Video + Audio")
        audio_label = row.params.get("audio_codec", "Copy")
        
        # Decide quality map locally
        is_cpu = "CPU" in codec_settings
        active_q_map = QUALITY_MAP_CPU if is_cpu else QUALITY_MAP_GPU
        
        f_count = len(self.window.file_manager.files)

        final_out_path, final_out_dir = utils.generate_output_path(
            row.path,
            active_q_map,
            q_label,
            f_count,
            OUTPUT_DIR_NAME,
            process_mode=mode_label,
            codec_key=codec_settings,
            audio_codec_key=audio_label,
        )
        row.out_path = Path(final_out_path)
        self.window.last_output_dir = final_out_dir

        cmd = build_ffmpeg_command(
            str(row.path),
            str(row.out_path),
            params["codec"],
            params["quality"],
            params["gpu"],
            width,
            input_codec,
            target_bitrate,
            max_bitrate,
            params["scale"],
            compression_level=params["compression_level"],
            process_mode=mode_label,
            audio_codec_key=audio_label,
        )

        parser = ProgressParser(duration, fps)

        row.log_data = [] # Reset log
        row.log_data.append(f"Command: {' '.join(cmd)}\n")
        ui(row.log_btn.set_visible, True)

        try:
            start_time = time.time()
            self.ffmpeg_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL, # Match original C++ logic
                stderr=subprocess.PIPE,    # Progress info via pipe:2
                stdin=subprocess.DEVNULL,
                universal_newlines=True,
                bufsize=1
            )

            # Pre-calculate file size and total pending duration for efficiency
            init_size = utils.get_file_size(row.path)
            init_size_str = utils.human_readable_size(init_size)
            
            # Sum durations of all pending files in the queue
            def _get_pending_dur():
                flist = self.window.file_manager.get_file_list()
                return sum(r.duration for r in flist[current_index+1:] if r.duration)
            
            pending_dur = _get_pending_dur()
            last_dur_check = time.time()

            last_ui_update = 0
            # iterate directly over stderr for maximum efficiency (no busy-waiting)
            for line in self.ffmpeg_process.stderr:
                if self.stop_requested:
                    self.ffmpeg_process.terminate()
                    break

                # Update UI periodically to reduce Gtk thread overhead
                progress = parser.parse(line)
                now = time.time()

                if progress:
                    if now - last_ui_update > 0.1: # Max 10 updates/sec
                        last_ui_update = now
                        pct, fps, speed, bitrate, rem = progress
                        # Calculate additional required parameters
                        # Calculate total queue ETA
                        q_rem = rem
                        effective_speed = speed if speed > 0.1 else 1.0

                        # Add estimated time for pending files
                        # Re-calculate pending duration only every few seconds or if it's 0
                        now_dur = time.time()
                        if now_dur - last_dur_check > 2.0:
                            pending_dur = _get_pending_dur()
                            last_dur_check = now_dur
                            
                        q_rem += pending_dur / effective_speed
                        # Calculate accurate estimated final size based on current output size
                        current_out_size = utils.get_file_size(row.out_path)
                        est_size = int(current_out_size / pct) if pct > 0.05 else 0 # Wait for 5% progress for stability
                        est_size_str = utils.human_readable_size(est_size) if est_size > 0 else "..."
                        ui(row.update_progress, pct, fps, speed, bitrate, rem, q_rem, init_size_str, est_size_str)

                        # Update Queue Status
                        bitrate_str = f"{bitrate:.0f} kbps" if bitrate > 0 else "N/A"
                        markup = (
                            f"<span size='medium' weight='bold' foreground='#ffb74d'>Queue ETA: {utils.format_time(q_rem)}</span>\n"
                            f"<span size='medium' weight='bold' foreground='#2ec27e'>Bitrate: {bitrate_str}</span>"
                        )
                        ui(self.queue_status.set_markup, markup)
                else:
                    # Only log lines that are actual output/errors, not progress lines
                    row.log_data.append(line.strip())

            self.ffmpeg_process.wait()
            elapsed = time.time() - start_time
            return_code = self.ffmpeg_process.returncode
            self.ffmpeg_process = None

            if return_code == 0 and not self.stop_requested:
                ui(self.window._handle_source_action, str(row.path))
                return elapsed, init_size, init_size_str

        except Exception as e:
            row.log_data.append(f"\nError: {e}")
            ui(row.set_error, f"Error: {str(e)[:30]}")
            
        return None

    def _on_queue_finished(self):
        self.window.start_btn.set_visible(True)
        self.window.stop_btn.set_visible(False)
        self.window.pause_btn.set_visible(False)
        self.window.add_btn.set_sensitive(True)
        self.window.open_out_btn.set_sensitive(True)
        self.window.queue_status.set_text("Idle")

        # Re-enable remove and unlock all reorders
        for row in self.window.file_manager.files.values():
            row.remove_btn.set_sensitive(True)
            row.set_reorder_locked(False)

        # Completion Action
        self.window._handle_completion()
