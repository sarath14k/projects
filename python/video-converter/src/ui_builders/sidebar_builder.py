"""Sidebar builder for configuration options."""

from gi.repository import Gtk, Pango
from ..config import (
    CODECS,
    AFTER_ACTIONS,
    AUTO_CLOSE_MAP,
    AFTER_COMPLETE,
    PROCESS_MODES,
    AUDIO_CODECS,
)

def build_sidebar(window):
    """Build the Bottom Shelf configuration and persistent bar.

    Args:
        window: The main VideoConverter window instance
    """
    main_vbox = window.vbox

    # Bottom Area Container
    window.bottom_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    window.bottom_area.get_style_context().add_class("bottom-bar")
    main_vbox.pack_end(window.bottom_area, False, False, 0)

    # 1. The Collapsible Shelf (Revealer)
    window.shelf_revealer = Gtk.Revealer()
    window.shelf_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_UP)
    window.shelf_revealer.set_transition_duration(300)
    window.bottom_area.pack_start(window.shelf_revealer, False, False, 0)

    shelf_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
    shelf_content.set_border_width(20)
    window.shelf_revealer.add(shelf_content)

    # GRID for settings
    grid = Gtk.Grid(column_spacing=20, row_spacing=15)
    shelf_content.add(grid)

    # Column 1
    from .. import utils
    window.gpu_device = Gtk.ComboBoxText()
    for path, label in utils.get_render_devices():
        window.gpu_device.append(path, label)
    window.gpu_device.set_active(0)
    _add_grid_field(grid, "GPU Device", window.gpu_device, 0, 0)

    window.codec = window._combo(list(CODECS.keys()), "codec", 0)
    window.codec.connect("changed", window.on_codec_changed)
    _add_grid_field(grid, "Codec", window.codec, 0, 1)

    window.quality = Gtk.ComboBoxText()
    _add_grid_field(grid, "Quality / Preset", window.quality, 0, 2)

    # Column 2
    window.scale_chk = Gtk.Switch()
    window.scale_chk.set_active(True)
    window.scale_chk.set_halign(Gtk.Align.START)
    _add_grid_field(grid, "Limit to 1080p", window.scale_chk, 1, 0)

    window.process_mode = window._combo(PROCESS_MODES, "process_mode", 0)
    _add_grid_field(grid, "Process Mode", window.process_mode, 1, 1)

    window.audio_codec = window._combo(list(AUDIO_CODECS.keys()), "audio_codec", 0)
    _add_grid_field(grid, "Audio Codec", window.audio_codec, 1, 2)

    # Column 3
    window.after_action = window._combo(AFTER_ACTIONS, "after_action", 0)
    _add_grid_field(grid, "Handling", window.after_action, 2, 0)

    window.auto_close = window._combo(AUTO_CLOSE_MAP, "auto_close", 0)
    _add_grid_field(grid, "Auto Close", window.auto_close, 2, 1)

    window.after_complete = window._combo(AFTER_COMPLETE, "after_complete", 0)
    _add_grid_field(grid, "Completion", window.after_complete, 2, 2)

    # Button Row in Shelf
    btn_box = Gtk.Box(spacing=10)
    shelf_content.pack_start(btn_box, False, False, 10)

    apply_all_btn = Gtk.Button(label="Apply to All Files")
    apply_all_btn.get_style_context().add_class("suggested-action")
    apply_all_btn.connect("clicked", lambda _: window.file_manager.apply_settings_to_all())
    btn_box.pack_start(apply_all_btn, True, True, 0)

    # 2. The Persistent Bottom Bar
    window.bottom_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    window.bottom_area.pack_start(window.bottom_sep, False, False, 0)

    window.bar_box = Gtk.Box(spacing=4)
    window.bar_box.set_border_width(8)
    window.bottom_area.pack_start(window.bar_box, False, False, 0)

    # Config Toggle
    window.config_toggle = Gtk.Button.new_from_icon_name("emblem-system-symbolic", Gtk.IconSize.BUTTON)
    window.config_toggle.set_tooltip_text("Toggle Configuration")
    window.config_toggle.get_style_context().add_class("flat-button")
    window.config_toggle.connect("clicked", lambda _: window.toggle_shelf(not window.shelf_visible))

    # Status Label
    window.queue_status = Gtk.Label(label="Ready.")
    window.queue_status.set_use_markup(True)
    window.queue_status.set_xalign(0)
    window.queue_status.set_ellipsize(Pango.EllipsizeMode.END)

    # Controls Box
    window.controls_box = Gtk.Box(spacing=6)
    
    window.stop_btn = Gtk.Button.new_from_icon_name("media-playback-stop-symbolic", Gtk.IconSize.BUTTON)
    window.stop_btn.get_style_context().add_class("destructive-action")
    window.stop_btn.connect("clicked", lambda _: window.conversion_manager.stop_encoding())
    window.controls_box.pack_start(window.stop_btn, False, False, 0)

    window.pause_btn = Gtk.Button.new_from_icon_name("media-playback-pause-symbolic", Gtk.IconSize.BUTTON)
    window.pause_btn.set_sensitive(False)
    window.pause_btn.connect("clicked", lambda _: window.conversion_manager.pause_resume())
    window.controls_box.pack_start(window.pause_btn, False, False, 0)

    window.start_btn = Gtk.Button.new_from_icon_name("media-playback-start-symbolic", Gtk.IconSize.BUTTON)
    window.start_btn.get_style_context().add_class("suggested-action")
    window.start_btn.connect("clicked", lambda _: window.conversion_manager.start_encoding())
    window.controls_box.pack_start(window.start_btn, False, False, 0)

    # Initial Layout
    update_bottom_bar_layout(window)

    # Trigger codec change to populate quality dropdown
    window.on_codec_changed(window.codec)

def update_bottom_bar_layout(window):
    """Switch bottom bar between horizontal and stacked layout."""
    is_compact = hasattr(window, "is_compact") and window.is_compact

    # Clear bar_box
    for child in window.bar_box.get_children():
        window.bar_box.remove(child)

    if is_compact:
        window.bar_box.set_orientation(Gtk.Orientation.VERTICAL)
        window.bar_box.set_spacing(8)
        
        # Row 1: Config Toggle + Status
        row1 = Gtk.Box(spacing=8)
        row1.pack_start(window.config_toggle, False, False, 0)
        row1.pack_start(window.queue_status, True, True, 0)
        window.bar_box.pack_start(row1, False, False, 0)
        
        # Row 2: Controls
        window.bar_box.pack_start(window.controls_box, False, False, 0)
        window.controls_box.set_halign(Gtk.Align.START)
    else:
        window.bar_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        window.bar_box.set_spacing(4)
        
        window.bar_box.pack_start(window.config_toggle, False, False, 0)
        window.bar_box.pack_start(window.queue_status, True, True, 0)
        window.bar_box.pack_end(window.controls_box, False, False, 0)
        window.controls_box.set_halign(Gtk.Align.END)

    window.bar_box.show_all()

def _add_grid_field(grid, label_text, widget, col, row):
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
    lbl = Gtk.Label(label=label_text.upper(), xalign=0)
    lbl.get_style_context().add_class("dim-label")
    box.pack_start(lbl, False, False, 0)
    box.pack_start(widget, False, False, 0)
    grid.attach(box, col, row, 1, 1)
