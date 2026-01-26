import os
from gi.repository import Gtk, GdkPixbuf, Pango, GLib, Gdk
from ..config import *
from ..utils import ui, THUMB_POOL
from ..engine import build_ffmpeg_command, ProgressParser

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
    )

    def __init__(self, path_str, remove_cb, move_up_cb, move_down_cb):
        self.path = path_str
        self.id = path_str
        self.log_data = ""
        self.pulse_id = None

        self.root = Gtk.ListBoxRow()
        self.root.set_selectable(False)
        self.root.get_style_context().add_class("row-card")

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        hbox.set_margin_top(4)
        hbox.set_margin_bottom(4)
        hbox.set_margin_start(4)
        hbox.set_margin_end(4)
        self.root.add(hbox)

        # Drag Handle
        handle = Gtk.EventBox()
        handle_icon = Gtk.Image.new_from_icon_name("open-menu-symbolic", Gtk.IconSize.MENU)
        handle_icon.set_opacity(0.3)
        handle.add(handle_icon)
        handle.set_tooltip_text("Drag to reorder")
        hbox.pack_start(handle, False, False, 0)

        # Thumbnail
        self.thumb = Gtk.Image()
        self.thumb.set_size_request(64, 64)
        self.thumb.get_style_context().add_class("thumbnail")
        hbox.pack_start(self.thumb, False, False, 0)

        # Info Box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        hbox.pack_start(vbox, True, True, 0)

        # Filename
        fname = os.path.basename(path_str)
        self.label = Gtk.Label(label=fname, xalign=0)
        self.label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        self.label.get_style_context().add_class("font-bold")
        vbox.pack_start(self.label, False, False, 0)

        self.info = Gtk.Label(label="Waiting...", xalign=0)
        self.info.get_style_context().add_class("dim-label")
        vbox.pack_start(self.info, False, False, 0)

        self.progress = Gtk.ProgressBar()
        vbox.pack_start(self.progress, False, False, 0)

        # Conflict Warning
        self.conflict = Gtk.Label(xalign=0)
        self.conflict.set_markup("<span foreground='#ffb74d' size='small'>⚠️ Output exists (will overwrite)</span>")
        self.conflict.set_no_show_all(True)
        self.conflict.set_visible(False)
        vbox.pack_start(self.conflict, False, False, 0)

        # Actions
        action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        
        # Log Button
        self.log_btn = Gtk.Button.new_from_icon_name("text-x-generic-symbolic", Gtk.IconSize.MENU)
        self.log_btn.get_style_context().add_class("flat-button")
        self.log_btn.set_tooltip_text("View Log")
        self.log_btn.connect("clicked", self.show_log)
        self.log_btn.set_no_show_all(True) # Hidden by default
        self.log_btn.set_visible(False)
        action_box.pack_start(self.log_btn, False, False, 0)

        # Remove
        self.remove_btn = Gtk.Button.new_from_icon_name("user-trash-symbolic", Gtk.IconSize.MENU)
        self.remove_btn.get_style_context().add_class("row-remove-btn")
        self.remove_btn.get_style_context().add_class("flat-button")
        self.remove_btn.set_tooltip_text("Remove")
        self.remove_btn.connect("clicked", lambda x: remove_cb(self.path))
        action_box.pack_start(self.remove_btn, False, False, 0)
        
        # Move Up/Down
        up_btn = Gtk.Button.new_from_icon_name("go-up-symbolic", Gtk.IconSize.MENU)
        up_btn.get_style_context().add_class("flat-button")
        up_btn.connect("clicked", lambda x: move_up_cb(self.path))
        action_box.pack_start(up_btn, False, False, 0)

        down_btn = Gtk.Button.new_from_icon_name("go-down-symbolic", Gtk.IconSize.MENU)
        down_btn.get_style_context().add_class("flat-button")
        down_btn.connect("clicked", lambda x: move_down_cb(self.path))
        action_box.pack_start(down_btn, False, False, 0)
        
        # Open/Play
        self.play_btn = Gtk.Button.new_from_icon_name("media-playback-start-symbolic", Gtk.IconSize.MENU)
        self.play_btn.get_style_context().add_class("flat-button")
        self.play_btn.set_tooltip_text("Open File")
        self.play_btn.connect("clicked", lambda x: ui(lambda: subprocess.Popen(["xdg-open", self.path])))
        self.play_btn.set_visible(False) # Only show on completion
        action_box.pack_start(self.play_btn, False, False, 0)

        hbox.pack_end(action_box, False, False, 0)

        THUMB_POOL.submit(self._generate_thumb)

    def show_log(self, btn):
        win = Gtk.Window(title=f"Log: {os.path.basename(self.path)}")
        win.set_default_size(600, 400)
        win.set_transient_for(btn.get_toplevel())
        win.set_modal(True)
        
        sw = Gtk.ScrolledWindow()
        tv = Gtk.TextView()
        tv.set_editable(False)
        tv.set_monospace(True)
        tv.get_buffer().set_text(self.log_data)
        
        sw.add(tv)
        win.add(sw)
        win.show_all()

    def _generate_thumb(self):
        cache_path = CACHE_DIR / (str(abs(hash(self.path))) + ".jpg")
        if not cache_path.exists():
            try:
                subprocess.run([
                    "ffmpeg", "-y", "-ss", "00:00:01", "-i", self.path,
                    "-vf", "scale=128:128:force_original_aspect_ratio=decrease",
                    "-vframes", "1", str(cache_path)
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass
        
        if cache_path.exists():
            ui(self._set_thumb, str(cache_path))

    def _set_thumb(self, path):
        try:
            pix = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, 64, 64, True)
            self.thumb.set_from_pixbuf(pix)
        except:
            pass

    def set_active(self, active):
        if active:
            self.root.get_style_context().add_class("active-row")
            self.label.get_style_context().add_class("activity-text")
        else:
            self.root.get_style_context().remove_class("active-row")
            self.label.get_style_context().remove_class("activity-text")

    def show_conflict(self):
        self.conflict.set_visible(True)
        self.conflict.show()

    def set_success(self):
        self.progress.get_style_context().add_class("success-bar")
