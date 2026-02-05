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
    BITRATE_MULTIPLIER_MAP,
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
        self.global_paused = False
        self.active_rows = []
        self.max_workers = 1 # Process 1 at a time as requested
        self.sleep_inhibitor = SleepInhibitor()
        self.queue_status = window.queue_status
        self.lock = threading.Lock()
        self.task_stats = {} # row -> {pct, speed, rem, bitrate}
        self.last_ui_update = 0

    def start_encoding(self):
        print("ConversionManager: start_encoding called", flush=True)
        with self.lock:
            self.stop_requested = False
            self.global_paused = False
            self.window.start_btn.set_visible(False)
            self.window.stop_btn.set_visible(True)
            self.window.stop_btn.set_sensitive(True)
            self.window.pause_btn.set_visible(True)
            self.window.pause_btn.set_sensitive(True)
            self.window.open_out_btn.set_sensitive(False)
            ui(self.window.global_progress.set_visible, True)
            ui(self.window.global_progress.set_fraction, 0)

            # Show controls for all pending/future rows
            for row in self.window.file_manager.files.values():
                if row.status == "pending":
                    ui(row.pause_row_btn.set_visible, True)
                    ui(row.stop_row_btn.set_visible, True)

        self.sleep_inhibitor.start()

        # Start Supervisor Thread
        t = threading.Thread(target=self._supervisor_loop, daemon=True)
        t.start()

    def stop_encoding(self):
        with self.lock:
            self.stop_requested = True
            # Stop all active processes
            for row in self.active_rows:
                if row.ffmpeg_process:
                    try:
                        row.ffmpeg_process.terminate()
                    except:
                        pass
            self.active_rows.clear()

        self.window.stop_btn.set_sensitive(False)
        self.window.pause_btn.set_sensitive(False)
        ui(self.queue_status.set_text, "Stopped")
        self.window.cancel_countdown()

        self.window.start_btn.set_visible(True)
        self.window.stop_btn.set_visible(False)
        self.window.pause_btn.set_visible(False)
        ui(self.window.global_progress.set_visible, False)

        for row in self.window.file_manager.files.values():
            if row.status in ["pending", "processing"]:
                ui(row.remove_btn.set_sensitive, True)
                ui(row.pause_row_btn.set_visible, False)
                ui(row.stop_row_btn.set_visible, False)

    def pause_resume(self):
        """Global pause/resume toggle."""
        with self.lock:
            self.global_paused = not self.global_paused
            state = self.global_paused
            
            icon = "media-playback-start-symbolic" if state else "media-playback-pause-symbolic"
            self.window.pause_btn.set_image(Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.BUTTON))
            ui(self.queue_status.set_text, "Paused" if state else "Processing...")

            for row in self.active_rows:
                self.pause_resume_row(row, force_state=state)

    def pause_resume_row(self, row, force_state=None):
        """Toggle pause for a specific row."""
        with self.lock:
            if force_state is not None:
                row.paused = force_state
            else:
                row.paused = not row.paused
            
            if row.ffmpeg_process:
                try:
                    os.kill(row.ffmpeg_process.pid, signal.SIGSTOP if row.paused else signal.SIGCONT)
                except:
                    pass
            
            icon = "media-playback-start-symbolic" if row.paused else "media-playback-pause-symbolic"
            ui(row.pause_row_btn.set_image, Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.BUTTON))

    def stop_row(self, row):
        """Stop/Cancel a specific row."""
        with self.lock:
            if row in self.active_rows:
                if row.ffmpeg_process:
                    try:
                        row.ffmpeg_process.terminate()
                    except:
                        pass
            elif row.status == "pending":
                # Mark as failed/cancelled so supervisor skips it
                row.status = "failed"
                ui(row.info.set_text, "Cancelled")
                ui(row.pause_row_btn.set_visible, False)
                ui(row.stop_row_btn.set_visible, False)
                ui(row.remove_btn.set_visible, True)

    def _supervisor_loop(self):
        while not self.stop_requested:
            try:
                file_list = self.window.file_manager.get_file_list()
                pending = [r for r in file_list if r.status == "pending"]
                print(f"ConversionManager: Loop - Pending: {len(pending)}, Active: {len(self.active_rows)}", flush=True)
                
                if not pending and not self.active_rows:
                    print("ConversionManager: No work left, stopping loop.", flush=True)
                    break
                
                # Fill active tasks up to max_workers
                with self.lock:
                    while len(self.active_rows) < self.max_workers and pending:
                        row = pending.pop(0)
                        row.status = "processing"
                        self.active_rows.append(row)
                        # Start worker thread for this row
                        try:
                            idx = file_list.index(row)
                            threading.Thread(target=self._encode_worker, args=(row, idx), daemon=True).start()
                        except Exception as e:
                            print(f"Failed to start worker: {e}", flush=True)
                            row.status = "failed"
                            if row in self.active_rows: self.active_rows.remove(row)
            except Exception as e:
                print(f"Supervisor loop error: {e}", flush=True)
            
            time.sleep(1)

        self.sleep_inhibitor.stop()
        ui(self._on_queue_finished)

    def _update_global_status(self, row, pct, fps, speed, bitrate, rem):
        """Called by workers to sync global UI with Total ETA."""
        with self.lock:
            self.task_stats[row] = {
                'pct': pct,
                'speed': speed,
                'rem': rem,
                'bitrate': bitrate
            }
            
            now = time.time()
            if now - self.last_ui_update < 0.2:
                return
            self.last_ui_update = now

        file_dict = self.window.file_manager.files
        total_files = len(file_dict)
        if total_files == 0: return

        # 1. Collective Progress
        sum_pct = 0
        active_rem_list = []
        avg_speed_sum = 0
        active_count = 0
        
        for r in file_dict.values():
            if r.status == "success":
                sum_pct += 1.0
            elif r in self.task_stats:
                stat = self.task_stats[r]
                sum_pct += stat['pct']
                active_rem_list.append(stat['rem'])
                avg_speed_sum += stat['speed']
                active_count += 1
        
        ui(self.window.global_progress.set_fraction, min(sum_pct / total_files, 1.0))

        # 2. Total ETA
        current_batch_rem = max(active_rem_list) if active_rem_list else 0
        pending_files = [r for r in file_dict.values() if r.status == "pending"]
        pending_dur = sum(r.duration for r in pending_files if r.duration)
        
        avg_speed = (avg_speed_sum / active_count) if active_count > 0 else 1.0
        effective_workers = min(self.max_workers, active_count + len(pending_files))
        pending_eta = (pending_dur / (effective_workers * avg_speed)) if (effective_workers > 0 and avg_speed > 0) else 0
        
        total_eta = current_batch_rem + pending_eta

        # 3. Markup
        markup = (
            f"<span size='medium' weight='bold' foreground='#ffb74d'>Total ETA: {utils.format_time(total_eta)}</span>\n"
            f"<span size='medium' weight='bold' foreground='#2ec27e'>Active: {active_count} | Speed: {avg_speed_sum:.1f}x</span>"
        )
        ui(self.queue_status.set_markup, markup)

    def _encode_worker(self, row, current_index):
        print(f"DEBUG: Worker for index {current_index} entered", flush=True)
        try:
            print(f"DEBUG: Updating UI for row {current_index}", flush=True)
            ui(row.set_active, True)
            ui(row.set_reorder_locked, True)
            ui(row.remove_btn.set_sensitive, False)
            
            # Ensure controls are visible
            ui(row.pause_row_btn.set_visible, True)
            ui(row.stop_row_btn.set_visible, True)

            result = self._encode_file(row, current_index)

            with self.lock:
                if row in self.active_rows:
                    self.active_rows.remove(row)
                if row in self.task_stats:
                    del self.task_stats[row]
                
                ui(row.set_active, False)
                ui(row.set_reorder_locked, False)
                ui(row.remove_btn.set_sensitive, True)
                ui(row.pause_row_btn.set_visible, False)
                ui(row.stop_row_btn.set_visible, False)

                if result is not None:
                    elapsed, init_size, init_size_str = result
                    ui(row.set_success)
                    from .. import utils
                    final_size = utils.get_file_size(row.out_path)
                    final_size_str = utils.human_readable_size(final_size)
                    diff = init_size - final_size
                    compression_pct = (diff / init_size * 100) if init_size > 0 else 0
                    ui(row.set_finished, elapsed, init_size_str, final_size_str, compression_pct)
                    ui(row.play_btn.set_visible, True)
                else:
                    if not self.stop_requested:
                        row.status = "failed"
                        ui(row.info.set_text, "Failed or Stopped")
        except Exception as e:
            print(f"Encode worker crashed: {e}")
            row.log_data.append(f"Worker Crash Error: {e}")
            row.status = "failed"
            if row in self.active_rows:
                with self.lock: self.active_rows.remove(row)
            ui(row.info.set_text, "Worker Error")
            ui(row.log_btn.set_visible, True)

    def _encode_file(self, row, current_index):
        # Resolve parameters from row.params
        p = row.params
        codec_key = p.get("codec_key", "HEVC (VAAPI 10-bit)")
        params = {
            "codec": CODECS.get(codec_key, CODECS["HEVC (VAAPI 10-bit)"]),
            "gpu": p.get("gpu", "cpu"),
            "scale": p.get("scale", True),
            "compression_level": DEFAULT_COMPRESSION_LEVEL
        }
        
        # Resolve quality value based on codec type
        q_map = QUALITY_MAP_CPU if "CPU" in codec_key else QUALITY_MAP_GPU
        params["quality"] = q_map.get(p.get("quality_text"), 23 if "CPU" not in codec_key else 6)

        # Get video info
        print(f"DEBUG: Getting video info for {row.path}", flush=True)
        duration, fps, input_codec, src_bitrate, width = utils.get_video_info(row.path)
        print(f"DEBUG: Info - Dur: {duration}, FPS: {fps}, Codec: {input_codec}", flush=True)

        # Calculate target and max bitrate (bits/s to match FFmpeg expectation)
        quality_val = params["quality"]
        multiplier = BITRATE_MULTIPLIER_MAP.get(quality_val, 0.5)
        # Match original C++ logic for minimum bitrate safety
        target_bitrate = max(int(src_bitrate * multiplier), 300_000)
        max_bitrate = max(int(target_bitrate * 1.5), 600_000)

        # Prepare output path and parameters
        codec_settings = row.params.get("codec_key", "HEVC (VAAPI 10-bit)")
        q_label = row.params.get("quality_text", "Main - 65% (QV-23)")
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
        print(f"Starting FFmpeg: {' '.join(cmd)}", flush=True)
        ui(row.log_btn.set_visible, True)

        try:
            print("DEBUG: Calling subprocess.Popen", flush=True)
            start_time = time.time()
            row.ffmpeg_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
                universal_newlines=True,
                bufsize=1
            )

            init_size = utils.get_file_size(row.path)
            init_size_str = utils.human_readable_size(init_size)
            
            for line in row.ffmpeg_process.stderr:
                print(f"FFMPEG_OUT: {line.strip()}", flush=True)
                if self.stop_requested or row.status == "failed":
                    row.ffmpeg_process.terminate()
                    break

                progress = parser.parse(line)

                if progress:
                    pct, fps, speed, bitrate, rem = progress
                    
                    # Update row UI
                    q_rem = rem # Per-row ETA
                    current_out_size = utils.get_file_size(row.out_path)
                    est_size = int(current_out_size / pct) if pct > 0.05 else 0
                    est_size_str = utils.human_readable_size(est_size) if est_size > 0 else "..."
                    ui(row.update_progress, pct, fps, speed, bitrate, rem, q_rem, init_size_str, est_size_str)

                    # Update Global UI
                    self._update_global_status(row, pct, fps, speed, bitrate, rem)
                else:
                    row.log_data.append(line.strip())

            row.ffmpeg_process.wait()
            elapsed = time.time() - start_time
            return_code = row.ffmpeg_process.returncode
            row.ffmpeg_process = None

            if return_code == 0 and not self.stop_requested:
                ui(self.window._handle_source_action, str(row.path))
                return elapsed, init_size, init_size_str

        except Exception as e:
            row.log_data.append(f"\nError: {e}")
            ui(row.info.set_text, "Error")
            
        return None

    def _on_queue_finished(self):
        self.window.start_btn.set_visible(True)
        self.window.stop_btn.set_visible(False)
        self.window.pause_btn.set_visible(False)
        self.window.open_out_btn.set_sensitive(True)
        ui(self.window.queue_status.set_text, "Idle")
        ui(self.window.global_progress.set_visible, False)

        # Re-enable remove and unlock all reorders
        for row in self.window.file_manager.files.values():
            ui(row.remove_btn.set_sensitive, True)
            ui(row.set_reorder_locked, False)

        # Completion Action
        ui(self.window._handle_completion)
