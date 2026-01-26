from gi.repository import Gtk, Gdk, GdkPixbuf, Pango, GLib
import os
import subprocess
from pathlib import Path

class VideoCard:
    def __init__(self, path_str, remove_cb=None):
        self.path = Path(path_str)
        self.id = path_str
        self.remove_cb = remove_cb
        self.full_pixbuf = None
        
        # State for Managers
        self.log_data = []
        self.duration = 0
        self.out_path = None
        
        # Build Widget
        self.root = Gtk.EventBox()
        self.root.file_row = self
        self.root.get_style_context().add_class("video-card")
        
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
        self.root.add(hbox)
        
        # Thumbnail
        self.thumb = Gtk.Image.new_from_icon_name("video-x-generic-symbolic", Gtk.IconSize.DIALOG)
        self.thumb.set_pixel_size(32)
        hbox.pack_start(self.thumb, False, False, 0)
        
        # Info Group
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        vbox.set_valign(Gtk.Align.CENTER)
        hbox.pack_start(vbox, True, True, 0)
        
        self.title = Gtk.Label(label=self.path.name)
        self.title.set_halign(Gtk.Align.START)
        self.title.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        self.title.set_width_chars(1)
        self.title.get_style_context().add_class("filename-label")
        vbox.pack_start(self.title, False, False, 0)
        
        # Sub-info
        details_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        vbox.pack_start(details_hbox, False, False, 0)
        
        self.meta = Gtk.Label(label="Analyzing...")
        self.meta.get_style_context().add_class("dim-label")
        self.meta.set_halign(Gtk.Align.START)
        details_hbox.pack_start(self.meta, False, False, 0)
        
        # Status Label
        self.status = Gtk.Label(label="READY")
        self.status.get_style_context().add_class("status-label")
        self.status.get_style_context().add_class("text-primary")
        hbox.pack_end(self.status, False, False, 0)

        # Mocks
        self.remove_btn = Gtk.Button()
        self.play_btn = Gtk.Button()
        self.info = self.meta

        # Trigger async data gathering
        GLib.idle_add(self._load_async_data)

    def _load_async_data(self):
        # 1. Gather duration
        from ..utils import get_video_info
        self.duration, _, _, _, _ = get_video_info(self.path)

        # 2. Extract Thumbnails (Two sizes: Queue and HQ Preview)
        thumb_dir = Path("/tmp/video_converter_thumbs")
        thumb_dir.mkdir(exist_ok=True)
        
        lo_res = thumb_dir / f"lo_{self.path.stem}.jpg"
        hi_res = thumb_dir / f"hi_{self.path.stem}.jpg"
        
        if not lo_res.exists():
            subprocess.run([
                "ffmpeg", "-ss", "5", "-i", str(self.path),
                "-vframes", "1", "-vf", "scale=160:-1",
                "-q:v", "4", str(lo_res)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        if not hi_res.exists():
            subprocess.run([
                "ffmpeg", "-ss", "5", "-i", str(self.path),
                "-vframes", "1", "-vf", "scale=1280:-1",
                "-q:v", "2", str(hi_res)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if lo_res.exists():
            try:
                lo_pix = GdkPixbuf.Pixbuf.new_from_file(str(lo_res))
                mini = lo_pix.scale_simple(36, 21, GdkPixbuf.InterpType.HYPER)
                self.thumb.set_from_pixbuf(mini)
            except: pass
            
        if hi_res.exists():
            try:
                self.full_pixbuf = GdkPixbuf.Pixbuf.new_from_file(str(hi_res))
            except: pass
            
        self.meta.set_text(self.path.suffix.upper()[1:] + " Video File")
        return False

    def set_active(self, active):
        if active: self.root.get_style_context().add_class("active-card")
        else: self.root.get_style_context().remove_class("active-card")

    def update_progress(self, pct, fps, speed, bitrate, rem, q_rem, in_size, out_size):
        self.status.set_text(f"{int(pct*100)}%")
        self.status.get_style_context().remove_class("text-success")
        self.status.get_style_context().add_class("text-primary")
        self.meta.set_text(f"{speed:.1f}x | {int(fps)}fps")

    def set_active_ui(self, is_active): self.set_active(is_active)
    def set_reorder_locked(self, locked): pass
    
    def set_success(self): 
        self.status.set_text("DONE")
        self.status.get_style_context().remove_class("text-primary")
        self.status.get_style_context().add_class("text-success")

    def show_conflict(self):
        self.status.set_text("EXISTS")
        self.status.get_style_context().add_class("text-warning")
