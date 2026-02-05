"""Theme manager for handling dark/pitch-black theme switching."""

from gi.repository import Gtk, Gdk
from ..css import PITCH_BLACK_CSS, STANDARD_CSS

def load_standard_css():
    """Load the standard gray theme CSS."""
    p = Gtk.CssProvider()
    p.load_from_data(STANDARD_CSS.encode("utf-8"))
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), p, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

def on_theme_toggled(window, switch, state):
    """Handle theme toggle switch.

    Args:
        window: The main VideoConverter window instance
        switch: The theme switch widget
        state: The new state (True = pitch black, False = standard dark)
    """
    settings = Gtk.Settings.get_default()

    # Always prefer dark theme (no more light mode)
    settings.set_property("gtk-application-prefer-dark-theme", True)
    settings.set_property("gtk-theme-name", "Adwaita-dark")

    # Apply pitch black override if enabled
    update_pitch_black_css(window, state)

    # Update label text
    if hasattr(window, 'theme_label'):
         window.theme_label.set_text("Black" if state else "Gray")

    return False

def update_pitch_black_css(window, enabled):
    """Update pitch black CSS provider.

    Args:
        window: The main VideoConverter window instance
        enabled: Whether to enable pitch black theme
    """
    if not hasattr(window, "pitch_black_provider"):
        window.pitch_black_provider = Gtk.CssProvider()
        window.pitch_black_provider.load_from_data(PITCH_BLACK_CSS.encode("utf-8"))

    # The add_btn was removed in favor of the FAB. No icon update needed here.
    
    screen = Gdk.Screen.get_default()
    if enabled:
        Gtk.StyleContext.add_provider_for_screen(
            screen, window.pitch_black_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION + 1
        )
    else:
        Gtk.StyleContext.remove_provider_for_screen(
            screen, window.pitch_black_provider
        )
