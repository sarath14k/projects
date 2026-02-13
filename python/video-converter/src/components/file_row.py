import os
import subprocess
import collections
import hashlib
from pathlib import Path
from gi.repository import Gtk, GdkPixbuf, Pango, GLib, Gdk
from ..config import *
from ..utils import ui, THUMB_POOL

class FileRow:
    __slots__ = (
        "path",
        "id",
        "root",
        "label",
        "remove_btn",
        "play_btn",
        "progress",
        "info",
        "conflict",
        "thumb",
        "log_btn",
        "log_data",
        "pulse_id",
        "handle",
        "duration",
        "out_path",
        "params",
        "settings_btn",
        "status",
    )

    def __init__(self, path_str, remove_cb, params=None, row_id=None):
        self.path = Path(path_str)
        self.out_path = None
        self.duration = None
        self.id = row_id or path_str
        self.params = params or {}
        self.status = "pending"
        self.log_data = collections.deque(maxlen=300)
        self.pulse_id = None

        # EventBox root for full-row dragging
        eb = Gtk.EventBox()
        eb.add_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.POINTER_MOTION_MASK)
        eb.get_style_context().add_class("row-card")
        self.root = eb

        frame = Gtk.Frame()
        eb.add(frame)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        hbox.set_border_width(8)
        frame.add(hbox)

        # Setup full-row drag source
        eb.drag_source_set(
            Gdk.ModifierType.BUTTON1_MASK,
            [Gtk.TargetEntry.new("row", 0, 0)],
            Gdk.DragAction.MOVE
        )
        eb.connect("drag-begin", self.on_drag_begin)
        eb.connect("drag-data-get", self.on_drag_data_get)

        # Cursor feedback for the whole row
        eb.connect("enter-notify-event", self._on_handle_enter)
        eb.connect("leave-notify-event", self._on_handle_leave)

        # Reference for locking (the whole EventBox)
        self.handle = eb

        # Thumbnail
        audio_exts = {".mp3", ".m4a", ".aac", ".flac", ".opus", ".wav", ".ogg"}
        is_audio = self.path.suffix.lower() in audio_exts
        icon = "audio-x-generic-symbolic" if is_audio else "video-x-generic-symbolic"

        self.thumb = Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.DIALOG)
        self.thumb.set_pixel_size(48)
        self.thumb.set_opacity(0.3)
        self.thumb.get_style_context().add_class("thumbnail")
        self.thumb.set_size_request(96, 54)
        hbox.pack_start(self.thumb, False, False, 0)

        # Content box (filename, info, progress)
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        hbox.pack_start(content_box, True, True, 0)

        # Top line with filename and conflict warning
        top_line = Gtk.Box(spacing=6)
        content_box.pack_start(top_line, False, False, 0)

        # Filename - 2 lines max with middle ellipsis
        fname = os.path.basename(path_str)
        self.label = Gtk.Label(label=fname, xalign=0)
        self.label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        self.label.set_lines(2)
        self.label.set_line_wrap(True)
        self.label.set_line_wrap_mode(Pango.WrapMode.CHAR)
        self.label.set_max_width_chars(30)
        self.label.get_style_context().add_class("font-bold")
        top_line.pack_start(self.label, True, True, 0)

        # Conflict Warning
        self.conflict = Gtk.Label()
        self.conflict.set_no_show_all(True)
        self.conflict.set_visible(False)
        top_line.pack_start(self.conflict, False, False, 0)

        # Info label
        self.info = Gtk.Label(label="Pending...", xalign=0)
        self.info.set_use_markup(True)
        self.info.get_style_context().add_class("dim-label")
        content_box.pack_start(self.info, False, False, 0)

        # Progress bar
        self.progress = Gtk.ProgressBar()
        self.progress.set_hexpand(True)
        content_box.pack_start(self.progress, False, False, 0)

        # Action buttons on the right (vertically stacked)
        action_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        action_box.set_valign(Gtk.Align.CENTER)

        # Play button
        self.play_btn = Gtk.Button.new_from_icon_name("media-playback-start-symbolic", Gtk.IconSize.BUTTON)
        self.play_btn.set_no_show_all(True)
        self.play_btn.set_visible(False)
        self.play_btn.connect("clicked", self._on_play)

        # Log button
        self.log_btn = Gtk.Button.new_from_icon_name("dialog-warning-symbolic", Gtk.IconSize.BUTTON)
        self.log_btn.set_no_show_all(True)
        self.log_btn.set_visible(False)
        self.log_btn.get_style_context().add_class("destructive-action")
        self.log_btn.connect("clicked", self.show_log)

        # Remove button
        self.remove_btn = Gtk.Button.new_from_icon_name("user-trash-symbolic", Gtk.IconSize.BUTTON)
        self.remove_btn.get_style_context().add_class("row-remove-btn")
        self.remove_btn.connect("clicked", lambda _: remove_cb(self.id))

        # Settings button
        self.settings_btn = Gtk.Button.new_from_icon_name("emblem-system-symbolic", Gtk.IconSize.BUTTON)
        self.settings_btn.set_tooltip_text("File Settings")
        self.settings_btn.connect("clicked", self.on_settings_clicked)

        action_box.pack_start(self.settings_btn, False, False, 0)
        action_box.pack_start(self.play_btn, False, False, 0)
        action_box.pack_start(self.log_btn, False, False, 0)
        action_box.pack_start(self.remove_btn, False, False, 0)
        hbox.pack_end(action_box, False, False, 0)

        if not is_audio:
            THUMB_POOL.submit(self._generate_thumb)

    def show_log(self, btn):
        dialog = Gtk.Dialog(title="FFmpeg Log", flags=0)
        dialog.add_buttons("Copy", 1, "Clear", 2, "Close", Gtk.ResponseType.CLOSE)
        dialog.set_default_size(700, 500)

        box = dialog.get_content_area()
        box.set_spacing(10)
        box.set_border_width(10)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)
        box.add(scrolled)

        text_view = Gtk.TextView()
        text_view.set_editable(False)
        text_view.set_monospace(True)
        log_text = "\n".join(self.log_data) if isinstance(self.log_data, list) else str(self.log_data)
        text_view.get_buffer().set_text(log_text)
        scrolled.add(text_view)

        dialog.show_all()
        while True:
            response = dialog.run()
            if response == 1:  # Copy
                clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
                clipboard.set_text(log_text, -1)
            elif response == 2:  # Clear
                self.log_data.clear()
                text_view.get_buffer().set_text("")
            else:
                break
        dialog.destroy()

    def _on_play(self, btn):
        target = str(self.out_path) if self.out_path else str(self.path)
        # Return False to stop GLib.idle_add loop
        ui(lambda: subprocess.Popen(["xdg-open", target]) and False)

    def _generate_thumb(self):
        try:
            # Fetch duration
            from .. import utils
            info = utils.get_video_info(str(self.path))
            self.duration = info[0]

            # Match original naming - use MD5 for cross-session stability
            h = hashlib.md5(str(self.path).encode()).hexdigest()
            thumb_path = CACHE_DIR / f"{h}.jpg"
            if not thumb_path.exists():
                import subprocess
                # Try original command: seek to 5s
                subprocess.run([
                    "ffmpeg", "-ss", "5", "-i", str(self.path),
                    "-vframes", "1", "-vf", "scale=192:-1",
                    "-q:v", "5", str(thumb_path)
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                # Fallback: if 5s seek failed (short video), try 0s
                if not thumb_path.exists():
                    subprocess.run([
                        "ffmpeg", "-ss", "0", "-i", str(self.path),
                        "-vframes", "1", "-vf", "scale=192:-1",
                        "-q:v", "5", str(thumb_path)
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            if thumb_path.exists():
                ui(self._set_thumb, str(thumb_path))
        except:
            pass

    def _set_thumb(self, path):
        try:
            # Match the set_size_request(96, 54)
            pix = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, 96, 54, True)
            self.thumb.set_from_pixbuf(pix)
            self.thumb.set_opacity(1.0)
        except:
            pass

    def set_active(self, active):
        if active:
            ui(self.root.get_style_context().add_class, "active-row")
            ui(self.label.get_style_context().add_class, "activity-text")
        else:
            ui(self.root.get_style_context().remove_class, "active-row")
            ui(self.label.get_style_context().remove_class, "activity-text")

    def show_conflict(self):
        self.conflict.set_markup("<span class='warning-text' size='small'>⚠ Overwrite</span>")
        self.conflict.show()

    def set_success(self):
        self.status = "completed"
        self.progress.get_style_context().remove_class("error-bar")
        self.progress.get_style_context().add_class("success-bar")

    def set_error(self, message="Error"):
        self.status = "failed"
        self.progress.get_style_context().remove_class("success-bar")
        self.progress.get_style_context().add_class("error-bar")
        self.info.set_markup(f"<span class='error-text'><b>{message}</b></span>")
        self.log_btn.set_visible(True)

    def set_reorder_locked(self, locked):
        if locked:
            self.root.drag_source_unset()
        else:
            self.root.drag_source_set(
                Gdk.ModifierType.BUTTON1_MASK,
                [Gtk.TargetEntry.new("row", 0, 0)],
                Gdk.DragAction.MOVE
            )

    def on_drag_begin(self, widget, context):
        # Create a nice drag icon
        from gi.repository import Gtk
        icon_box = Gtk.Box(spacing=10)
        icon_box.set_border_width(6)
        icon_box.get_style_context().add_class("row-card")

        lbl = Gtk.Label(label=os.path.basename(str(self.path)))
        icon_box.add(lbl)
        icon_box.show_all()

        Gtk.drag_set_icon_widget(context, icon_box, 0, 0)

    def on_drag_data_get(self, widget, context, data, info, time):
        # Set the file ID as the drag data
        data.set(Gdk.Atom.intern_static_string("row"), 8, str(self.id).encode())

    def _on_handle_enter(self, widget, event):
        window = widget.get_window()
        if window:
            cursor = Gdk.Cursor.new_from_name(Gdk.Display.get_default(), "move")
            window.set_cursor(cursor)

    def _on_handle_leave(self, widget, event):
        window = widget.get_window()
        if window:
            window.set_cursor(None)

    def update_progress(self, pct, fps, speed, bitrate, rem, q_rem, init_size_str, est_size_str):
        if self.pulse_id:
            GLib.source_remove(self.pulse_id)
            self.pulse_id = None

        self.progress.set_fraction(pct)
        from .. import utils
        markup = (
            f"<span size='large'><b>{int(pct * 100)}%</b> • <span class='accent-text'>{fps:.0f} fps</span> • <span class='info-text'>x{speed:.1f}</span> • "
            f"<span class='warning-text'>ETA: {utils.format_time(rem)}</span></span>\n"
            f"<span size='medium' alpha='80%'>{init_size_str} ➝ <span class='info-text'>{est_size_str}</span></span>"
        )
        self.info.set_markup(markup)

    def set_finished(self, elapsed_time, initial_size_str, final_size_str, compression_pct):
        self.progress.set_fraction(1.0)
        from .. import utils
        
        # Color the compression percent based on performance
        cls = "success-text" if compression_pct > 30 else "accent-text"
        if compression_pct < 0: cls = "error-text"
        
        # Ensure status is updated thread-safely if called from thread
        self.status = "completed"
        
        markup = (
            f"<span size='large' class='success-text'>Completed in {utils.format_time(elapsed_time)}</span>\n"
            f"<span size='medium' alpha='80%'>{initial_size_str} ➝ <span class='accent-text'><b>{final_size_str}</b></span> "
            f"(<span class='{cls}'><b>-{compression_pct:.1f}%</b></span>)</span>"
        )
        self.info.set_markup(markup)

    def on_settings_clicked(self, btn):
        dialog = FileSettingsDialog(self.root.get_toplevel(), self.params)
        if dialog.run() == Gtk.ResponseType.OK:
            self.params = dialog.get_params()
            # Re-check conflict if settings changed (though out_path depends on quality)
            # For simplicity, we can let FileManager handle update if needed, 
            # but current architecture calculates out_path just before encoding or on add.
            # We should probably update the out_path or at least visual indicators here if needed.
        dialog.destroy()

class FileSettingsDialog(Gtk.Dialog):
    def __init__(self, parent, params):
        Gtk.Dialog.__init__(self)
        self.set_title("File Conversion Settings")
        self.set_transient_for(parent)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(400, -1)
        
        self.params = params.copy()
        
        box = self.get_content_area()
        box.set_spacing(10)
        box.set_border_width(15)
        
        from ..config import CODECS, QUALITY_MAP_GPU, QUALITY_MAP_CPU
        from .. import utils
        
        # GPU Device
        self.gpu_device = Gtk.ComboBoxText()
        for path, label in utils.get_render_devices():
            self.gpu_device.append(path, label)
        self.gpu_device.set_active_id(self.params.get("gpu", "cpu"))
        self._add_row(box, "GPU Device", self.gpu_device)
        
        # Codec
        self.codec = Gtk.ComboBoxText()
        for c in CODECS.keys():
            self.codec.append_text(c)
        self.codec.set_active_id(self.params.get("codec_key", "HEVC (VAAPI 10-bit)"))
        # ComboBoxText set_active_id works only if strings are added properly as IDs.
        # Let's fix that by searching for index.
        self._set_combo_text(self.codec, self.params.get("codec_key"))
        self.codec.connect("changed", self.on_codec_changed)
        self._add_row(box, "Codec", self.codec)
        
        # Quality
        self.quality = Gtk.ComboBoxText()
        self._add_row(box, "Quality / Preset", self.quality)

        # Scale
        self.scale_chk = Gtk.Switch()
        self.scale_chk.set_active(self.params.get("scale", True))
        self.scale_chk.set_halign(Gtk.Align.START)
        self._add_row(box, "Limit to 1080p", self.scale_chk)

        # Process Mode
        from ..config import PROCESS_MODES, AUDIO_CODECS

        self.process_mode = Gtk.ComboBoxText()
        for mode in PROCESS_MODES:
            self.process_mode.append_text(mode)
        self._set_combo_text(self.process_mode, self.params.get("process_mode", "Video + Audio"))
        self._add_row(box, "Process Mode", self.process_mode)

        # Audio Codec
        self.audio_codec = Gtk.ComboBoxText()
        for c in AUDIO_CODECS.keys():
            self.audio_codec.append_text(c)
        self._set_combo_text(
            self.audio_codec, self.params.get("audio_codec", "Copy")
        )
        self._add_row(box, "Audio Codec", self.audio_codec)
        
        # Initial quality populate
        self.on_codec_changed(self.codec)
        self._set_combo_text(self.quality, self.params.get("quality_text"))
        
        self.show_all()

    def _add_row(self, box, label, widget):
        row = Gtk.Box(spacing=10)
        lbl = Gtk.Label(label=label, xalign=0)
        lbl.set_size_request(150, -1)
        row.pack_start(lbl, False, False, 0)
        row.pack_start(widget, True, True, 0)
        box.pack_start(row, False, False, 0)

    def _set_combo_text(self, combo, text):
        if not text: return
        model = combo.get_model()
        for i, row in enumerate(model):
            if row[0] == text:
                combo.set_active(i)
                break

    def on_codec_changed(self, combo):
        codec_key = combo.get_active_text()
        from ..config import QUALITY_MAP_GPU, QUALITY_MAP_CPU
        new_map = QUALITY_MAP_CPU if "CPU" in codec_key else QUALITY_MAP_GPU
        
        self.quality.remove_all()
        sorted_items = sorted(new_map.items(), key=lambda item: item[1])
        for k, v in sorted_items:
            self.quality.append_text(k)
        self.quality.set_active(0)

    def get_params(self):
        return {
            "gpu": self.gpu_device.get_active_id(),
            "codec_key": self.codec.get_active_text(),
            "quality_text": self.quality.get_active_text(),
            "scale": self.scale_chk.get_active(),
            "process_mode": self.process_mode.get_active_text(),
            "audio_codec": self.audio_codec.get_active_text(),
        }
