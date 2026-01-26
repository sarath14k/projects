from gi.repository import Gtk, Pango
from ..config import QUALITY_MAP_GPU, AFTER_ACTIONS, AFTER_COMPLETE, AUTO_CLOSE_MAP

def build_inspector(window):
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    box.get_style_context().add_class("inspector-pane")
    
    # 1. Preview Area - Compact margins
    preview_root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    preview_root.set_margin_top(8)
    preview_root.set_margin_bottom(12)
    preview_root.set_margin_start(8)
    preview_root.set_margin_end(8)
    preview_root.get_style_context().add_class("immersive-preview-bg")

    window.preview_frame = Gtk.EventBox()
    window.preview_frame.get_style_context().add_class("studio-preview-frame")
    
    window.preview_image = Gtk.Image()
    window.preview_frame.add(window.preview_image)
    preview_root.pack_start(window.preview_frame, False, False, 0)
    box.pack_start(preview_root, False, False, 0)
    
    # 2. Metadata Area - Minimal margins
    meta_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
    meta_box.set_margin_start(10)
    meta_box.set_margin_end(10)
    meta_box.set_margin_bottom(10)
    
    window.info_filename = Gtk.Label(label="Preview")
    window.info_filename.get_style_context().add_class("inspector-filename")
    window.info_filename.set_halign(Gtk.Align.START)
    window.info_filename.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
    window.info_filename.set_max_width_chars(15)
    meta_box.pack_start(window.info_filename, False, False, 0)
    
    window.info_details = Gtk.Label(label="Select a file...")
    window.info_details.get_style_context().add_class("dim-label")
    window.info_details.set_halign(Gtk.Align.START)
    window.info_details.set_ellipsize(Pango.EllipsizeMode.END)
    window.info_details.set_max_width_chars(20)
    meta_box.pack_start(window.info_details, False, False, 0)
    box.pack_start(meta_box, False, False, 0)
    
    # 3. Settings Area - Compact
    settings_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    settings_box.set_margin_start(10)
    settings_box.set_margin_end(10)
    settings_box.set_margin_bottom(10)
    box.pack_start(settings_box, True, True, 0)

    def add_field(label_text, widget):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        lbl = Gtk.Label(label=label_text)
        lbl.set_halign(Gtk.Align.START)
        lbl.get_style_context().add_class("dim-label")
        lbl.set_width_chars(6)
        row.pack_start(lbl, False, False, 0)
        row.pack_end(widget, True, True, 0)
        settings_box.pack_start(row, False, False, 0)

    window.codec = Gtk.ComboBoxText()
    for c in ["HEVC (VAAPI 10-bit)", "AV1 (VAAPI 10-bit)"]: window.codec.append_text(c)
    window.codec.set_active(0)
    window.codec.connect("changed", window.on_codec_changed)
    add_field("Engine", window.codec)

    window.quality = Gtk.ComboBoxText()
    for k in QUALITY_MAP_GPU.keys(): window.quality.append_text(k)
    window.quality.set_active(2)
    add_field("Quality", window.quality)

    window.after_action = Gtk.ComboBoxText()
    for a in AFTER_ACTIONS: window.after_action.append_text(a)
    window.after_action.set_active(0)
    add_field("Then", window.after_action)

    window.auto_close = Gtk.ComboBoxText()
    for a in AFTER_COMPLETE: window.auto_close.append_text(a)
    window.auto_close.set_active(0)
    add_field("Finish", window.auto_close)

    window.scale_chk = Gtk.CheckButton(label="Upscale")
    settings_box.pack_start(window.scale_chk, False, False, 0)

    # 4. Action Buttons - Compact
    actions_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
    actions_box.set_margin_start(10)
    actions_box.set_margin_end(10)
    actions_box.set_margin_bottom(10)
    
    def create_btn(label, icon, cb, cls):
        btn = Gtk.Button()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        hbox.pack_start(Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.SMALL_TOOLBAR), False, False, 0)
        lbl = Gtk.Label(label=label)
        lbl.set_ellipsize(Pango.EllipsizeMode.END)
        hbox.pack_start(lbl, False, False, 0)
        btn.add(hbox)
        btn.get_style_context().add_class("btn")
        btn.get_style_context().add_class(cls)
        btn.connect("clicked", cb)
        return btn

    window.btn_log = create_btn("Logs", "utilities-terminal-symbolic", lambda _: window.show_log(window.selected_row), "btn-outline-secondary")
    window.btn_play = create_btn("Preview", "media-playback-start-symbolic", lambda _: window.open_file(window.selected_row), "btn-primary")
    window.btn_remove = create_btn("Remove", "edit-delete-symbolic", lambda _: window.file_manager.remove_file(window.selected_row.path if window.selected_row else None), "btn-danger")

    actions_box.pack_start(window.btn_log, False, False, 0)
    actions_box.pack_start(window.btn_play, False, False, 0)
    actions_box.pack_start(window.btn_remove, False, False, 0)
    box.pack_end(actions_box, False, False, 0)
    
    window.inspector_actions = actions_box
    window.inspector_actions.set_sensitive(False)
    
    return box
