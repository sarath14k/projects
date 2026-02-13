"""Header bar builder for the video converter UI."""

from gi.repository import Gtk

def build_header(window):
    """Build and configure the header bar with theme switcher.

    Args:
        window: The main VideoConverter window instance
    """
    header = Gtk.HeaderBar()
    header.set_show_close_button(True)
    header.props.title = "Video Converter"
    window.set_titlebar(header)

    # Hamburger menu button
    window.hamburger_btn = Gtk.Button.new_from_icon_name(
        "open-menu-symbolic", Gtk.IconSize.MENU
    )
    window.hamburger_btn.connect(
        "clicked", lambda _: window.toggle_sidebar(not window.sidebar_visible)
    )
    header.pack_start(window.hamburger_btn)

    # Theme Switcher
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    box.set_valign(Gtk.Align.CENTER)

    icon = Gtk.Image.new_from_icon_name("preferences-desktop-theme-symbolic", Gtk.IconSize.MENU)

    window.theme_switch = Gtk.Switch()
    window.theme_switch.set_valign(Gtk.Align.CENTER)
    window.theme_switch.connect("state-set", window.on_theme_toggled)

    # Dynamic label: "Light" (Standard Dark) vs "Dark" (Pitch Black)
    window.theme_label = Gtk.Label(label="Light")

    box.pack_start(icon, False, False, 0)
    box.pack_start(window.theme_label, False, False, 0)
    box.pack_start(window.theme_switch, False, False, 0)

    header.pack_end(box)
