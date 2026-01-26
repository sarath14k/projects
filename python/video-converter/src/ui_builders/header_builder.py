"""Header bar builder for the video converter UI."""

from gi.repository import Gtk

def build_header(window):
    """Build and configure the header bar with colorful icon-only controls."""
    header = Gtk.HeaderBar()
    header.set_show_close_button(True)
    header.props.title = "Video Converter"
    window.set_titlebar(header)

    def create_icon_btn(icon, cb, cls=None, tooltip=None):
        btn = Gtk.Button.new_from_icon_name(icon, Gtk.IconSize.BUTTON)
        btn.get_style_context().add_class("btn")
        if cls: btn.get_style_context().add_class(cls)
        if tooltip: btn.set_tooltip_text(tooltip)
        btn.connect("clicked", cb)
        return btn

    # --- Left Side: File Actions ---
    btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    
    # Add Files
    window.add_btn = create_icon_btn("list-add-symbolic", window.pick_files, "btn-outline-secondary", "Add Files")
    btn_box.pack_start(window.add_btn, False, False, 0)
    
    # Clear All
    window.clear_btn = create_icon_btn("edit-clear-all-symbolic", lambda _: window.file_manager.clear_all(), "btn-icon", "Clear Queue")
    btn_box.pack_start(window.clear_btn, False, False, 0)
    
    header.pack_start(btn_box)

    # --- Right Side: Conversion Actions ---
    
    # Open Output
    window.open_out_btn = create_icon_btn("folder-open-symbolic", window.open_output_folder, "btn-icon", "Open Output Folder")
    window.open_out_btn.set_sensitive(False)
    header.pack_end(window.open_out_btn)

    # Theme Switcher
    theme_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    theme_box.set_valign(Gtk.Align.CENTER)
    window.theme_switch = Gtk.Switch()
    window.theme_switch.connect("state-set", window.on_theme_toggled)
    window.theme_label = Gtk.Label(label="Pitch")
    theme_box.pack_start(window.theme_label, False, False, 0)
    theme_box.pack_start(window.theme_switch, False, False, 0)
    header.pack_end(theme_box)

    # Stop Button
    window.stop_btn = create_icon_btn("media-playback-stop-symbolic", lambda _: window.conversion_manager.stop_encoding(), "btn-danger", "Stop")
    header.pack_end(window.stop_btn)

    # Pause Button
    window.pause_btn = create_icon_btn("media-playback-pause-symbolic", lambda _: window.conversion_manager.pause_resume(), "btn-outline-secondary", "Pause/Resume")
    header.pack_end(window.pause_btn)

    # Start Button
    window.start_btn = create_icon_btn("media-playback-start-symbolic", lambda x: window.start_encoding(x), "btn-success", "Start Conversion")
    window.start_btn.set_sensitive(False)
    header.pack_end(window.start_btn)

    header.show_all()
    window.stop_btn.hide()
    window.pause_btn.hide()
    
    return header
