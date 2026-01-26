"""Sidebar builder for configuration options."""

from gi.repository import Gtk
from ..config import CODECS, AFTER_ACTIONS, AUTO_CLOSE_MAP, AFTER_COMPLETE

def build_sidebar(window):
    """Build the configuration sidebar with all options.

    Args:
        window: The main VideoConverter window instance
    """
    # Get main_hbox from window (should be created before calling this)
    main_hbox = window.main_hbox

    # Sidebar revealer
    window.sidebar_revealer = Gtk.Revealer()
    window.sidebar_revealer.set_transition_type(
        Gtk.RevealerTransitionType.SLIDE_RIGHT
    )
    window.sidebar_revealer.set_transition_duration(250)
    window.sidebar_revealer.set_reveal_child(True)
    main_hbox.pack_start(window.sidebar_revealer, False, False, 0)

    sidebar_frame = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    sidebar_frame.set_size_request(200, -1)
    sidebar_frame.get_style_context().add_class("sidebar-bg")
    window.sidebar_revealer.add(sidebar_frame)

    # Header
    header_box = Gtk.Box(spacing=16)
    header_box.set_border_width(20)
    app_title = Gtk.Label(xalign=0)
    app_title.set_markup("<span weight='heavy' size='large'>Configuration</span>")
    header_box.pack_start(app_title, True, True, 0)
    sidebar_frame.pack_start(header_box, False, False, 0)

    # Scrollable content
    side_scroll = Gtk.ScrolledWindow()
    side_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    sidebar_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
    sidebar_content.set_border_width(20)
    side_scroll.add(sidebar_content)
    sidebar_frame.pack_start(side_scroll, True, True, 0)

    # GPU Device
    from .. import utils
    window.gpu_device = Gtk.ComboBoxText()
    for path, label in utils.get_render_devices():
        window.gpu_device.append(path, label)
    window.gpu_device.set_active(0)
    window._add_field(sidebar_content, "GPU Device", window.gpu_device)

    # Codec
    window.codec = window._combo(list(CODECS.keys()), "codec", 0)
    window.codec.connect("changed", window.on_codec_changed)
    window._add_field(sidebar_content, "Codec", window.codec)

    # Quality
    window.quality = Gtk.ComboBoxText()
    window._add_field(sidebar_content, "Quality / Preset", window.quality)

    # Scale checkbox
    window.scale_chk = Gtk.Switch()
    window.scale_chk.set_active(True)
    window.scale_chk.set_halign(Gtk.Align.START)
    window._add_field(sidebar_content, "Limit to 1080p", window.scale_chk)

    # After action
    window.after_action = window._combo(AFTER_ACTIONS, "after_action", 0)
    window._add_field(sidebar_content, "Handling", window.after_action)

    # Auto close
    window.auto_close = window._combo(AUTO_CLOSE_MAP, "auto_close", 0)
    window._add_field(sidebar_content, "Auto Close", window.auto_close)

    # After complete
    window.after_complete = window._combo(AFTER_COMPLETE, "after_complete", 0)
    window._add_field(sidebar_content, "Completion", window.after_complete)

    # Trigger codec change to populate quality dropdown
    window.on_codec_changed(window.codec)
