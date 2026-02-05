"""Sidebar builder for configuration options."""

from gi.repository import Gtk
from ..config import (
    CODECS,
    AFTER_ACTIONS,
    AUTO_CLOSE_MAP,
    AFTER_COMPLETE,
    PROCESS_MODES,
    AUDIO_CODECS,
)


def _add_accordion_section(window, container, title, icon_name, open_by_default=False):
    """Adds a collapsible section to the sidebar."""
    section_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    section_vbox.get_style_context().add_class("glass-section")
    
    # Header button
    header_btn = Gtk.Button()
    header_btn.get_style_context().add_class("accordion-header")
    
    h_box = Gtk.Box(spacing=8)
    icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.MENU)
    lbl = Gtk.Label()
    lbl.set_markup(f"<b>{title.upper()}</b>")
    lbl.get_style_context().add_class("dim-label")
    
    arrow = Gtk.Image.new_from_icon_name("pan-down-symbolic", Gtk.IconSize.MENU)
    
    h_box.pack_start(icon, False, False, 0)
    h_box.pack_start(lbl, True, True, 0)
    h_box.pack_start(arrow, False, False, 0)
    header_btn.add(h_box)
    
    section_vbox.pack_start(header_btn, False, False, 0)
    
    # Revealer for content
    revealer = Gtk.Revealer()
    revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
    revealer.set_reveal_child(open_by_default)
    
    # Update arrow on reveal
    def toggle_reveal(_):
        is_open = not revealer.get_reveal_child()
        revealer.set_reveal_child(is_open)
        arrow.set_from_icon_name(
            "pan-up-symbolic" if is_open else "pan-down-symbolic", Gtk.IconSize.MENU
        )
    
    header_btn.connect("clicked", toggle_reveal)
    
    content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    content_box.set_border_width(8)
    revealer.add(content_box)
    section_vbox.pack_start(revealer, False, False, 0)
    
    container.pack_start(section_vbox, False, False, 0)
    return content_box

def build_sidebar(window):
    """Build the configuration sidebar with all options.

    Args:
        window: The main VideoConverter window instance
    """
    # Get main_hbox from window (should be created before calling this)
    main_hbox = window.main_hbox

    # Sidebar revealer
    window.sidebar_revealer = Gtk.Revealer()
    window.sidebar_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_RIGHT)
    window.sidebar_revealer.set_transition_duration(250)
    window.sidebar_revealer.set_reveal_child(True)
    main_hbox.pack_start(window.sidebar_revealer, False, False, 0)

    sidebar_frame = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    sidebar_frame.set_size_request(200, -1)
    sidebar_frame.get_style_context().add_class("sidebar-bg")
    window.sidebar_revealer.add(sidebar_frame)

    # Header
    header_box = Gtk.Box(spacing=12)
    header_box.set_border_width(12)
    app_title = Gtk.Label(xalign=0)
    app_title.set_markup("<span weight='heavy' size='18000' alpha='90%'>Config</span>")
    header_box.pack_start(app_title, True, True, 0)
    sidebar_frame.pack_start(header_box, False, False, 0)

    # Scrollable content
    side_scroll = Gtk.ScrolledWindow()
    side_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    sidebar_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    sidebar_content.set_border_width(12)
    side_scroll.add(sidebar_content)
    sidebar_frame.pack_start(side_scroll, True, True, 0)

    # 1. Hardware Section
    hardware_box = _add_accordion_section(window, sidebar_content, "Hardware", "computer-symbolic", True)
    
    from .. import utils
    window.gpu_device = Gtk.ComboBoxText()
    for path, label in utils.get_render_devices():
        window.gpu_device.append(path, label)
    window.gpu_device.set_active(0)
    window._add_field(hardware_box, "Render Device", window.gpu_device)

    # 2. Video Section
    video_box = _add_accordion_section(window, sidebar_content, "Video", "video-x-generic-symbolic", True)

    window.codec = window._combo(list(CODECS.keys()), "codec", 0)
    window.codec.connect("changed", window.on_codec_changed)
    window._add_field(video_box, "Codec", window.codec)

    window.quality = Gtk.ComboBoxText()
    window._add_field(video_box, "Quality / Preset", window.quality)

    window.scale_chk = Gtk.Switch()
    window.scale_chk.set_active(True)
    window.scale_chk.set_halign(Gtk.Align.START)
    window._add_field(video_box, "Limit to 1080p", window.scale_chk)

    # 3. Audio Section
    audio_box = _add_accordion_section(window, sidebar_content, "Audio", "audio-x-generic-symbolic")

    window.process_mode = window._combo(PROCESS_MODES, "process_mode", 0)
    window._add_field(audio_box, "Process Mode", window.process_mode)

    window.audio_codec = window._combo(list(AUDIO_CODECS.keys()), "audio_codec", 0)
    window._add_field(audio_box, "Audio Codec", window.audio_codec)

    # 4. Automation Section
    auto_box = _add_accordion_section(window, sidebar_content, "Automation", "system-run-symbolic")

    window.after_action = window._combo(AFTER_ACTIONS, "after_action", 0)
    window._add_field(auto_box, "Post-Process", window.after_action)

    window.auto_close = window._combo(AUTO_CLOSE_MAP, "auto_close", 0)
    window._add_field(auto_box, "Auto Close", window.auto_close)

    window.after_complete = window._combo(AFTER_COMPLETE, "after_complete", 0)
    window._add_field(auto_box, "System Action", window.after_complete)

    # Apply to all button (at the bottom, not in accordion)
    sidebar_content.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 12)
    apply_all_btn = Gtk.Button(label="Apply to All Files")
    apply_all_btn.get_style_context().add_class("suggested-action")
    apply_all_btn.set_margin_top(12)
    apply_all_btn.connect(
        "clicked", lambda _: window.file_manager.apply_settings_to_all()
    )
    sidebar_content.pack_start(apply_all_btn, False, False, 0)

    # Trigger codec change to populate quality dropdown
    window.on_codec_changed(window.codec)
