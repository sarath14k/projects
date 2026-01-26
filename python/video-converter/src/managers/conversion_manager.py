import time
import subprocess
import signal
import threading
import os
from pathlib import Path
from gi.repository import GLib, Gtk

from ..engine import build_ffmpeg_command, ProgressParser
from ..utils import ui, SleepInhibitor
from ..config import AUTO_CLOSE_MAP

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
        self.window.add_btn.set_sensitive(False)
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
        file_list = self.window.file_manager.get_file_list()
        total = len(file_list)

        for i, row in enumerate(file_list):
            if self.stop_requested:
                break
            # Skip if file was removed from queue while paused or running
            if row.id not in self.window.file_manager.files:
                continue

            self.current_file_row = row
            path = row.path

            ui(row.set_active, True)
            ui(row.set_reorder_locked, True)
            ui(row.remove_btn.set_sensitive, False)
            ui(self.queue_status.set_text, f"Processing {i+1} of {total}...")

            # Scroll to row
            # adj = self.window.file_list_box.get_adjustment() ... (UI logic mostly)

            self._encode_file(row, file_list, i)

            ui(row.set_active, False)
            ui(row.set_reorder_locked, False)
            ui(row.remove_btn.set_sensitive, True)
            
            # Final UI cleanup for this file
            ui(row.update_progress, 1.0, 0, 0, 0, 0, 0, "...", "...") # Ensure 100% and clean labels
            ui(row.set_success)
            ui(row.info.set_text, "Completed")
            ui(row.play_btn.set_visible, True)

            # Post-action per file? (Not implemented in original fully for each file, mostly for queue)

        self.sleep_inhibitor.stop()
        ui(self._on_queue_finished)

    def _encode_file(self, row, file_list, current_index):
        params = {}
        # We need a way to get params synchronously from UI thread.
        # Hack: generic getter

        done = threading.Event()
        def get_params():
            # Get codec configuration
            codec_key = self.window.codec.get_active_text()
            from ..config import CODECS, BITRATE_MULTIPLIER_MAP
            params["codec"] = CODECS[codec_key]
            params["quality"] = self.window.active_quality_map.get(self.window.quality.get_active_text(), 26)
            params["gpu"] = self.window.gpu_device.get_active_id()
            params["scale"] = self.window.scale_chk.get_active()
            done.set()

        GLib.idle_add(get_params)
        done.wait()

        # Get video info
        from .. import utils
        duration, fps, input_codec, src_bitrate, width = utils.get_video_info(row.path)

        # Calculate target and max bitrate (bits/s to match FFmpeg expectation)
        from ..config import BITRATE_MULTIPLIER_MAP
        quality_val = params["quality"]
        multiplier = BITRATE_MULTIPLIER_MAP.get(quality_val, 0.5)
        # Match original C++ logic for minimum bitrate safety
        target_bitrate = max(int(src_bitrate * multiplier), 300_000)
        max_bitrate = max(int(target_bitrate * 1.5), 600_000)

        # Generate output path using shared utility
        quality_map = self.window.active_quality_map
        quality_text = self.window.quality.get_active_text()
        from ..config import OUTPUT_DIR_NAME
        file_count = len(self.window.file_manager.files)

        out_path, _ = utils.generate_output_path(
            row.path, quality_map, quality_text, file_count, OUTPUT_DIR_NAME
        )
        row.out_path = Path(out_path)

        cmd = build_ffmpeg_command(
            str(row.path),
            str(out_path),
            params["codec"],
            params["quality"],
            params["gpu"],
            width,
            input_codec,
            target_bitrate,
            max_bitrate,
            params["scale"]
        )

        parser = ProgressParser(duration, fps)

        row.log_data = [] # Reset log
        row.log_data.append(f"Command: {' '.join(cmd)}\n")
        ui(row.log_btn.set_visible, True)

        try:
            self.ffmpeg_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL, # Match original C++ logic
                stderr=subprocess.PIPE,    # Progress info via pipe:2
                stdin=subprocess.DEVNULL,
                universal_newlines=True,
                bufsize=1
            )

            # Pre-calculate file size for loop optimization
            from .. import utils
            init_size = utils.get_file_size(row.path)
            init_size_str = utils.human_readable_size(init_size)

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
                        for j in range(current_index + 1, len(file_list)):
                            next_row = file_list[j]
                            # Durations should be available from FileRow (populated on add)
                            # If not, fallback to current file's duration as estimate
                            next_dur = next_row.duration if next_row.duration else duration
                            q_rem += next_dur / effective_speed
                        est_size = int(init_size * pct) if pct > 0 else 0
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
            return_code = self.ffmpeg_process.returncode
            self.ffmpeg_process = None

            if return_code == 0 and not self.stop_requested:
                ui(self.window._handle_source_action, str(row.path))

        except Exception as e:
            row.log_data.append(f"\nError: {e}")
            ui(row.info.set_text, "Error")

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
