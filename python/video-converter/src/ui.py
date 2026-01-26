import os
import signal
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from gi.repository import Gdk, GdkPixbuf, GLib, Gtk, Pango

from .config import *
from .engine import ProgressParser, build_ffmpeg_command
from .utils import SleepInhibitor, ui, THUMB_POOL
from .css import PITCH_BLACK_CSS
from .components.file_row import FileRow
from . import utils

from .managers.prefs_manager import PrefsManager
from .managers.file_manager import FileManager
from .managers.conversion_manager import ConversionManager

from .ui_builders import header_builder, sidebar_builder, main_area_builder, theme_manager

class VideoConverter(Gtk.Window):
    def __init__(self):
        super().__init__(title="Video Converter")
        # FIXED: Use set_prgname instead of deprecated set_wmclass
        GLib.set_prgname(APP_NAME)

        self.set_default_size(950, 650)
        self.set_border_width(0)

        self.sidebar_visible = True
        self.files = {} # Keep compatibility if needed, but managers handle it
        self.last_folder = str(Path.home())
        self.last_output_dir = None
        self.rem_sec = 0
        self.countdown_source_id = None
        self.config = {} # Initialize config for _combo usage
        self.proc = None  # Track encoding process state (compatibility)
        self.active_quality_map = QUALITY_MAP_GPU  # Initialize with default quality map

        self._init_ui()
        self._init_shortcuts()

        # Initialize managers AFTER UI is created
        self.prefs_manager = PrefsManager(self)
        self.file_manager = FileManager(self)
        self.conversion_manager = ConversionManager(self)

        self.drag_dest_set(
            Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY
        )
        self.drag_dest_add_uri_targets()
        self.connect("drag-motion", self.on_drag_motion)
        self.connect("drag-leave", self.on_drag_leave)
        self.connect("drag-data-received", self.on_drag_data_received)

        # Load Preferences
        self.prefs_manager.load_prefs()
        self.connect("delete-event", self.on_quit_attempt)

        self.show_all()
        # Deferred UI restore and initial state update
        self.prefs_manager.restore_ui_state()
        self._update_empty_state()

        # Apply theme label
        pitch = self.theme_switch.get_active()
        self.theme_label.set_text("Black" if pitch else "Gray")

    def on_quit_attempt(self, widget, event):
        if self.conversion_manager.ffmpeg_process:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.YES_NO,
                text="Encoding in Progress",
            )
            dialog.format_secondary_text("Are you sure you want to quit?")
            if dialog.run() == Gtk.ResponseType.YES:
                self.cleanup()
                Gtk.main_quit()
            dialog.destroy()
            return True
        Gtk.main_quit()
        return False

    def cleanup(self):
        self.prefs_manager.save_prefs()
        THUMB_POOL.shutdown(wait=False)

    def _init_ui(self):
        """Initialize the UI using modular builders."""
        # Load standard theme first
        theme_manager.load_standard_css()

        # Build header with theme switcher
        header_builder.build_header(self)

        # Create overlay and main container
        self.overlay = Gtk.Overlay()
        self.add(self.overlay)

        self.main_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.overlay.add(self.main_hbox)

        # Build sidebar with configuration options
        sidebar_builder.build_sidebar(self)
        main_area_builder.build_main_area(self)

    def _init_shortcuts(self):
        self.connect("key-press-event", self.on_key_press)

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_o and (event.state & Gdk.ModifierType.CONTROL_MASK):
            self.pick_files(None)
            return True
        if event.keyval == Gdk.KEY_q and (event.state & Gdk.ModifierType.CONTROL_MASK):
            self.on_quit_attempt(self, None)
            return True
        if event.keyval in [Gdk.KEY_Return, Gdk.KEY_KP_Enter] and (
            event.state & Gdk.ModifierType.CONTROL_MASK
        ):
            if self.file_manager.files and not self.conversion_manager.ffmpeg_process:
                self.conversion_manager.start_encoding()
            return True
        return False

    def toggle_sidebar(self, show):
        self.sidebar_revealer.set_reveal_child(show)
        self.sidebar_visible = show
        self.queue_draw()

    def _update_empty_state(self):
        # Check FileManager's files, not self.files (which is for compatibility only)
        files_count = len(self.file_manager.files) if hasattr(self, 'file_manager') else len(self.files)
        if files_count > 0:
            self.stack.set_visible_child_name("list")
        else:
            self.stack.set_visible_child_name("empty")
        self.start_btn.set_sensitive(files_count > 0)

    def _add_field(self, container, label_text, widget):
        lbl = Gtk.Label(label=label_text.upper(), xalign=0)
        lbl.get_style_context().add_class("dim-label")
        container.pack_start(lbl, False, False, 0)
        container.pack_start(widget, False, False, 0)

    def _combo(self, values, config_key, default_val):
        c = Gtk.ComboBoxText()
        for v in values:
            c.append_text(v)
        c.set_active(self.config.get(config_key, default_val))
        return c

    def on_codec_changed(self, combo):
        codec_key = combo.get_active_text()
        if not codec_key:
            return
        if "CPU" in codec_key:
            new_map = QUALITY_MAP_CPU
            default_val = 6
        else:
            new_map = QUALITY_MAP_GPU
            default_val = 26

        self.active_quality_map = new_map
        self.quality.remove_all()
        sorted_items = sorted(new_map.items(), key=lambda item: item[1])
        for k, v in sorted_items:
            self.quality.append_text(k)

        self.quality.set_active(0)
        for i, (k, v) in enumerate(sorted_items):
            if v == default_val:
                self.quality.set_active(i)
                break

    def open_output_folder(self, _):
        if self.last_output_dir:
            utils.open_folder_safe(self.last_output_dir)

    def on_drag_motion(self, widget, context, x, y, time):
        self.stack.get_style_context().add_class("drag-active")
        Gdk.drag_status(context, Gdk.DragAction.COPY, time)
        return True

    def on_drag_leave(self, widget, context, time):
        self.stack.get_style_context().remove_class("drag-active")

    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        self.stack.get_style_context().remove_class("drag-active")
        self.file_manager.process_dropped_data(data)
        Gtk.drag_finish(drag_context, True, False, time)

    def pick_files(self, _):
        dlg = Gtk.FileChooserDialog(
            title="Select Videos", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dlg.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        dlg.set_select_multiple(True)
        if self.last_folder:
            dlg.set_current_folder(self.last_folder)
        if dlg.run() == Gtk.ResponseType.OK:
            self.last_folder = dlg.get_current_folder()
            self.file_manager.add_files(dlg.get_filenames())
        dlg.destroy()

    def _handle_source_action(self, path):
        idx = self.after_action.get_active()
        try:
            if idx == 1:
                subprocess.run(["trash-put", path], check=True)
            elif idx == 2:
                os.remove(path)
        except Exception as e:
            utils.send_notification("Error", f"Failed to remove source: {e}")

    def _handle_completion(self):
        utils.send_notification("Conversion Complete", "All tasks finished.")
        if self.after_complete.get_active() == 1:
            self.start_countdown(
                60, "Shutdown in", lambda: subprocess.run(["systemctl", "poweroff"])
            )
        sec = AUTO_CLOSE_MAP.get(self.auto_close.get_active_text(), 0)
        if sec > 0:
            self.start_countdown(sec, "Closing in", Gtk.main_quit)

    def start_countdown(self, seconds, prefix, callback):
        self.cancel_countdown()  # Cancel any existing countdown first
        self.rem_sec = seconds

        def _tick():
            if self.rem_sec > 0:
                self.queue_status.set_markup(
                    f"<span size='x-large' weight='bold' foreground='#ffb74d'>{prefix} {self.rem_sec}s... (Stop to cancel)</span>"
                )
                self.rem_sec -= 1
                return True
            callback()
            return False

        self.countdown_source_id = GLib.timeout_add(1000, _tick)

    def cancel_countdown(self):
        """Cancel any running countdown (auto-close/shutdown)."""
        if self.countdown_source_id:
            GLib.source_remove(self.countdown_source_id)
            self.countdown_source_id = None
            self.queue_status.set_markup("<span size='large' weight='bold' foreground='#2ec27e'>Countdown canceled.</span>")

    def on_theme_toggled(self, switch, state):
        """Delegate to theme manager."""
        return theme_manager.on_theme_toggled(self, switch, state)

    def _update_pitch_black_css(self, enabled):
        """Delegate to theme manager."""
        theme_manager.update_pitch_black_css(self, enabled)
