from gi.repository import Gtk, Gdk, GLib, Pango, GdkPixbuf
import os
from .ui_builders import theme_manager, header_builder, queue_builder, inspector_builder
from .components.video_card import VideoCard
from .managers.file_manager import FileManager
from .managers.conversion_manager import ConversionManager
from .utils import ui
from .config import QUALITY_MAP_GPU, QUALITY_MAP_CPU

class VideoConverter(Gtk.Window):
    def __init__(self):
        super().__init__(title="Video Converter")
        self.set_default_size(1100, 700)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # UI State
        self.selected_row = None
        self.active_quality_map = QUALITY_MAP_GPU # Default
        self.gpu_device_path = "/dev/dri/renderD128" # Default internal
        
        # Core Managers
        self.file_manager = FileManager(self)
        
        self._init_ui()
        
        # Managers needing UI components
        self.conversion_manager = ConversionManager(self)
        
        self.connect("destroy", Gtk.main_quit)
        self.connect("configure-event", self.on_configure)
        self.show_all()

    def _init_ui(self):
        theme_manager.load_standard_css()
        
        # Header Bar
        self.header = header_builder.build_header(self)
        self.set_titlebar(self.header)
        
        # Main Layout
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # Add slight margin to body
        main_vbox.set_margin_top(4)
        self.add(main_vbox)

        # Paned (60/40)
        self.paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.paned.get_style_context().add_class("main-split")
        main_vbox.pack_start(self.paned, True, True, 0)
        
        self.queue_container = queue_builder.build_queue(self)
        self.paned.pack1(self.queue_container, True, True)

        # Right: Inspector (Scrollable for narrow viewports)
        inspector_internal = inspector_builder.build_inspector(self)
        self.inspector_scrolled = Gtk.ScrolledWindow()
        self.inspector_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.inspector_scrolled.add(inspector_internal)
        self.inspector_container = self.inspector_scrolled
        self.paned.pack2(self.inspector_container, True, True)
        
        # Status Bar
        self.status_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.status_bar.get_style_context().add_class("status-bar")
        self.queue_status = Gtk.Label(label="Ready")
        self.status_bar.pack_start(self.queue_status, False, False, 10)
        main_vbox.pack_end(self.status_bar, False, False, 0)

    def on_configure(self, widget, event):
        """Bootstrap-style Responsive Stacking & Relative Scaling."""
        width = event.width
        height = event.height
        ctx = self.get_style_context()
        
        # 1. Always Horizontal - just adjust proportions
        if self.paned.get_orientation() == Gtk.Orientation.VERTICAL:
            self.paned.set_orientation(Gtk.Orientation.HORIZONTAL)
        
        # 2. Ultra-Micro Breakpoint (1/8 screen) - 80/20 split
        if width < 550:
            self.paned.set_position(int(width * 0.8))
            if not ctx.has_class("tiny-window"): ctx.add_class("tiny-window")
            if ctx.has_class("small-window"): ctx.remove_class("small-window")
        # 3. Small Breakpoint - 65/35 split
        elif width < 960:
            self.paned.set_position(int(width * 0.65))
            if not ctx.has_class("small-window"): ctx.add_class("small-window")
            if ctx.has_class("tiny-window"): ctx.remove_class("tiny-window")
        # 4. Normal - 70/30 split
        else:
            self.paned.set_position(int(width * 0.7))
            if ctx.has_class("small-window"): ctx.remove_class("small-window")
            if ctx.has_class("tiny-window"): ctx.remove_class("tiny-window")

        # 3. Relative Content Scaling
        # Determine available inspector width based on orientation
        if self.paned.get_orientation() == Gtk.Orientation.HORIZONTAL:
            insp_w = int(width * 0.3)
        else:
            insp_w = width # In vertical mode, inspector gets full width
            
        if hasattr(self, "selected_row") and self.selected_row:
             self._update_inspector(self.selected_row)
             
        return False

    def on_row_selected(self, listbox, row_container):
        if not row_container: return
        # Logic to extract the VideoCard object from the list row
        card_root = row_container.get_child()
        if hasattr(card_root, "file_row"):
            self.selected_row = card_root.file_row
            self._update_inspector(self.selected_row)

    def _update_inspector(self, row):
        if not row: return
        
        # Calculate target preview width based on current window/pane size
        width, _ = self.get_size()
        if self.paned.get_orientation() == Gtk.Orientation.HORIZONTAL:
            insp_w = int(width * 0.3)
        else:
            insp_w = width
        
        target_w = max(100, min(int((insp_w - 32) * 0.98), 500))
        target_h = int(target_w * 0.5625) # 16:9

        self.info_filename.set_text(row.path.name)
        self.info_details.set_text(f"{row.path.suffix.upper()[1:]} | Studio Preview Ready")
        
        # High-res Studio Preview
        if hasattr(row, "full_pixbuf") and row.full_pixbuf:
             scaled = row.full_pixbuf.scale_simple(target_w, target_h, GdkPixbuf.InterpType.HYPER)
             self.preview_image.set_from_pixbuf(scaled)
        else:
             self.preview_image.set_from_icon_name("video-x-generic-symbolic", Gtk.IconSize.DIALOG)
             self.preview_image.set_pixel_size(target_w)
             
        self.inspector_actions.set_sensitive(True)

    # --- Callbacks ---
    def pick_files(self, *args):
        dialog = Gtk.FileChooserDialog(
            title="Choose video files", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        dialog.set_select_multiple(True)
        
        filter_any = Gtk.FileFilter()
        filter_any.set_name("Video files")
        filter_any.add_mime_type("video/*")
        dialog.add_filter(filter_any)

        if dialog.run() == Gtk.ResponseType.OK:
            self.file_manager.add_files(dialog.get_filenames())
        dialog.destroy()

    def start_encoding(self, *args):
        if self.file_manager.files:
            self.conversion_manager.start_encoding()

    def open_output_folder(self, *args):
        os.system('xdg-open "Converted" &')

    def on_theme_toggled(self, switch, state):
        theme_manager.update_pitch_black_css(self, state)
        if state:
            self.theme_label.set_text("Pitch")
        else:
            self.theme_label.set_text("Dark")

    def on_codec_changed(self, combo):
        text = combo.get_active_text()
        if "VAAPI" in text:
            self.active_quality_map = QUALITY_MAP_GPU
        else:
            self.active_quality_map = QUALITY_MAP_CPU
        
        # Refresh Quality combo
        self.quality.remove_all()
        for k in self.active_quality_map.keys():
            self.quality.append_text(k)
        self.quality.set_active(2)

    def _update_empty_state(self):
        """Toggle placeholder when queue is empty."""
        has_files = bool(self.file_manager.files)
        self.empty_label.set_visible(not has_files)
        self.file_list.set_visible(has_files)

    def show_log(self, row):
        if not row: return
        dialog = Gtk.MessageDialog(parent=self, modal=True, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text=f"Logs: {row.path.name}")
        log_view = Gtk.TextView()
        log_view.get_style_context().add_class("monospace")
        log_view.set_editable(False)
        
        log_text = "\\n".join(row.log_data) if row.log_data else "No logs available."
        log_view.get_buffer().set_text(log_text)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_min_content_height(400)
        scrolled.set_min_content_width(700)
        scrolled.add(log_view)
        dialog.get_content_area().pack_start(scrolled, True, True, 0)
        dialog.show_all()
        dialog.run()
        dialog.destroy()

    def open_file(self, row):
        if row: os.system(f'xdg-open "{row.path}" &')

    def cancel_countdown(self, *args): 
        # For auto-shutdown logic (not fully implemented in this minimalist rebuild)
        pass
        
    def _handle_source_action(self, source_path):
        action = self.after_action.get_active_text()
        if action == "Delete Source":
            try: os.remove(source_path)
            except: pass
        elif action == "Move to Trash":
            try: os.system(f'gio trash "{source_path}"')
            except: pass

    def _handle_completion(self):
        self.queue_status.set_text("Queue Finished.")
        action = self.auto_close.get_active_text()
        if action == "Quit App":
            Gtk.main_quit()
        elif action == "Shutdown":
            os.system("shutdown now")
        elif action == "Suspend":
             os.system("systemctl suspend")
