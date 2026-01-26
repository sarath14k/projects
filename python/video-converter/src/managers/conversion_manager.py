import time
import subprocess
import signal
import threading
import os
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
        self.window.pause_btn.set_visible(True)
        self.window.add_btn.set_sensitive(False)
        self.window.open_out_btn.set_sensitive(False) 
        
        # Disable remove buttons
        for row in self.window.file_manager.files.values():
            row.remove_btn.set_sensitive(False)

        self.sleep_inhibitor.start()
        
        # Start Thread
        t = threading.Thread(target=self._run_queue, daemon=True)
        t.start()

    def stop_encoding(self):
        self.stop_requested = True
        self.current_file_row = None
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()
        
        self.window.stop_btn.set_sensitive(False)
        self.window.pause_btn.set_sensitive(False)
        self.queue_status.set_text("Stopping...")

    def pause_resume(self):
        self.paused = not self.paused
        if self.paused:
            if self.ffmpeg_process:
                os.kill(self.ffmpeg_process.pid, signal.SIGSTOP)
            self.window.pause_btn.set_icon_name("media-playback-start-symbolic")
            self.queue_status.set_text("Paused")
        else:
            if self.ffmpeg_process:
                os.kill(self.ffmpeg_process.pid, signal.SIGCONT)
            self.window.pause_btn.set_icon_name("media-playback-pause-symbolic")
            self.queue_status.set_text("Processing...")

    def _run_queue(self):
        file_list = self.window.file_manager.get_file_list()
        total = len(file_list)
        
        for i, row in enumerate(file_list):
            if self.stop_requested:
                break
                
            self.current_file_row = row
            path = row.path
            
            ui(row.set_active, True)
            ui(self.queue_status.set_text, f"Processing {i+1} of {total}...")
            
            # Scroll to row
            # adj = self.window.file_list_box.get_adjustment() ... (UI logic mostly)
            
            self._encode_file(row)
            
            ui(row.set_active, False)
            ui(row.set_success)
            ui(row.info.set_text, "Completed")
            ui(row.play_btn.set_visible, True)
            
            # Post-action per file? (Not implemented in original fully for each file, mostly for queue)
            
        self.sleep_inhibitor.stop()
        ui(self._on_queue_finished)

    def _encode_file(self, row):
        # Gather encoding parameters from UI (via window)
        try:
            # We need to access UI elements safely using ui() for values?
            # Actually reading values from widgets in a background thread is UNSAFE in GTK.
            # We should gather them before starting or use GLib.invoke to fetch.
            # BUT, existing code likely did it or cached it.
            # For safety, let's look at how original code did it.
            # Original code accessed self.codec.get_active() inside encode_file likely.
            pass
        except:
            pass
            
        # To keep it simple and safe, we will gather params on main thread before this call
        # OR use invoke_and_wait pattern.
        # Let's assume for now we call a helper on main thread to get params.
        
        # Wait... the manager runs in a thread.
        # We should capture the settings at the start of the batch?
        # Or Just Get them via idle_add wait?
        
        # simpler: The PrefsManager/UI already has the values.
        # Accessing Gtk Properties from thread is generally bad but reading strings usually doesn't crash immediately,
        # but usage of get_active_text() might.
        
        params = {}
        # We need a way to get params synchronously from UI thread.
        # Hack: generic getter
        
        done = threading.Event()
        def get_params():
            params["codec"] = self.window.codec.get_active_id()
            params["quality"] = self.window.quality.get_active_id()
            params["gpu"] = self.window.gpu_device.get_active_text()
            # Scale check
            params["scale"] = self.window.scale_chk.get_active()
            done.set()
            
        GLib.idle_add(get_params)
        done.wait()
        
        out_path = self.window._get_out_path(row.path)
        
        cmd = build_ffmpeg_command(
            str(row.path),
            str(out_path),
            params["codec"],
            params["quality"],
            params["gpu"],
            params["scale"]
        )
        
        parser = ProgressParser(self.window._filesize(row.path))
        
        row.log_data = [] # Reset log
        row.log_data.append(f"Command: {' '.join(cmd)}\n")
        ui(row.log_btn.set_visible, True)
        
        try:
            self.ffmpeg_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            for line in self.ffmpeg_process.stdout:
                if self.stop_requested:
                    self.ffmpeg_process.terminate()
                    break
                
                row.log_data.append(line.strip())
                
                # Update UI ~10 times/sec max ideally, but here line by line
                progress = parser.parse(line)
                if progress:
                     ui(self.window._update_row_ui, row, *progress)
                     
            self.ffmpeg_process.wait()
            self.ffmpeg_process = None
            
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
        
        # Re-enable remove
        for row in self.window.file_manager.files.values():
            row.remove_btn.set_sensitive(True)
            
        # Completion Action
        self.window._handle_completion()
