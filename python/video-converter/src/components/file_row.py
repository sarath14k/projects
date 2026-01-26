import os
import subprocess
import collections
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
        "progress",
        "info",
        "conflict",
        "thumb",
        "log_data",
        "pulse_id",
        "handle",
        "duration",
        "out_path",
        "remove_btn",
        "play_btn",
        "log_btn",
        "full_pixbuf",
    )

    def __init__(self, path_str, remove_cb):
        self.path = Path(path_str)
        self.out_path = None
        self.duration = None
        self.id = path_str
        self.log_data = collections.deque(maxlen=300)
        self.pulse_id = None
        self.full_pixbuf = None

        # EventBox for interaction (Click/Drag)
        eb = Gtk.EventBox()
        eb.get_style_context().add_class("row-card")
        self.root = eb
        
        # We don't need complex drag logic here for internal widgets
        # The ListBox will mostly handle selection.
        # But for drag-reorder, we still might want source set.
        # Actually, let's keep it simple: ListBoxRow handles selection.
        # We just provide the visual content.
        
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        hbox.set_border_width(0)
        eb.add(hbox)

        # Thumbnail (Small & Minimal)
        self.thumb = Gtk.Image.new_from_icon_name("video-x-generic-symbolic", Gtk.IconSize.DIALOG)
        self.thumb.set_pixel_size(48)
        self.thumb.set_opacity(0.1)
        self.thumb.get_style_context().add_class("thumbnail")
        self.thumb.set_size_request(80, 48)
        hbox.pack_start(self.thumb, False, False, 0)
        
        # Info Box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        vbox.set_valign(Gtk.Align.CENTER)
        hbox.pack_start(vbox, True, True, 0)

        # Filename
        fname = os.path.basename(path_str)
        self.label = Gtk.Label(label=fname, xalign=0)
        self.label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        self.label.set_width_chars(1) # Allow shrinking
        self.label.get_style_context().add_class("filename-label")
        vbox.pack_start(self.label, False, False, 0)

        # Status & Progress Area
        status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        vbox.pack_start(status_box, False, False, 0)
        
        self.info = Gtk.Label(label="Pending", xalign=0)
        self.info.get_style_context().add_class("dim-label")
        status_box.pack_start(self.info, False, False, 0)

        self.progress = Gtk.ProgressBar()
        self.progress.set_hexpand(True)
        self.progress.set_valign(Gtk.Align.CENTER)
        status_box.pack_start(self.progress, True, True, 0)

        self.conflict = Gtk.Label()
        self.conflict.set_no_show_all(True)
        self.conflict.set_visible(False)
        status_box.pack_end(self.conflict, False, False, 0)

        # Compatibility placeholders
        self.remove_btn = Gtk.Button()
        self.play_btn = Gtk.Button()
        self.log_btn = Gtk.Button()
        self.remove_btn.set_no_show_all(True)
        self.play_btn.set_no_show_all(True)
        self.log_btn.set_no_show_all(True)

        THUMB_POOL.submit(self._generate_thumb)

    def _generate_thumb(self):
        try:
            from .. import utils
            info = utils.get_video_info(str(self.path))
            self.duration = info[0]

            thumb_path = CACHE_DIR / f"{abs(hash(str(self.path)))}.jpg"
            if not thumb_path.exists():
                import subprocess
                subprocess.run([
                    "ffmpeg", "-ss", "5", "-i", str(self.path),
                    "-vframes", "1", "-vf", "scale=640:-1",
                    "-q:v", "2", str(thumb_path)
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            if thumb_path.exists():
                ui(self._set_thumb, str(thumb_path))
        except:
            pass

    def _set_thumb(self, path):
        try:
            # Load full res (640px)
            self.full_pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
            
            # Scale down for list view
            pix = self.full_pixbuf.scale_simple(80, 48, GdkPixbuf.InterpType.HYPER)
            self.thumb.set_from_pixbuf(pix)
            self.thumb.set_opacity(1.0)
        except:
            pass

    def set_active(self, active):
        if active:
            self.root.get_style_context().add_class("active-row")
        else:
            self.root.get_style_context().remove_class("active-row")

    def show_conflict(self):
        self.conflict.set_markup("<span foreground='#f39c12' weight='bold' size='small'>⚠ Exist</span>")
        self.conflict.show()

    def set_success(self):
        self.progress.get_style_context().add_class("success-bar")

    def set_reorder_locked(self, locked):
        """Placeholder for reorder locking."""
        pass

    def show_log(self, _):
        """Show FFmpeg log in a dialog."""
        dialog = Gtk.MessageDialog(
            transient_for=self.root.get_toplevel(),
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=f"Log: {os.path.basename(str(self.path))}",
        )
        scroll = Gtk.ScrolledWindow()
        scroll.set_size_request(600, 400)
        tv = Gtk.TextView()
        tv.set_editable(False)
        tv.get_buffer().set_text("\n".join(self.log_data))
        scroll.add(tv)
        dialog.get_content_area().pack_start(scroll, True, True, 0)
        dialog.show_all()
        dialog.run()
        dialog.destroy()

    def update_progress(self, pct, fps, speed, bitrate, rem, q_rem, init_size_str, est_size_str):
        if self.pulse_id:
            GLib.source_remove(self.pulse_id)
            self.pulse_id = None

        self.progress.set_fraction(pct)
        # Show detailed info: percentage, speed, fps, and bitrate
        bitrate_str = f"{bitrate:.0f}kbps" if bitrate > 0 else "N/A"
        info_text = f"{int(pct*100)}% | {speed:.1f}x | {bitrate_str}"
        if fps > 0:
            info_text += f" | {int(fps)}fps"
        self.info.set_text(info_text)
