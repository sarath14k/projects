"""Theme manager for handling dark/pitch-black theme switching."""

from gi.repository import Gtk, Gdk
from ..css import PITCH_BLACK_CSS


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
         window.theme_label.set_text("Dark" if state else "Light")
    
    return False
    
    # Force redraw to apply custom CSS correctly if needed
    window.queue_draw()


def update_pitch_black_css(window, enabled):
    """Update pitch black CSS provider.
    
    Args:
        window: The main VideoConverter window instance
        enabled: Whether to enable pitch black theme
    """
    if not hasattr(window, "pitch_black_provider"):
        window.pitch_black_provider = Gtk.CssProvider()
        window.pitch_black_provider.load_from_data(PITCH_BLACK_CSS.encode("utf-8"))

    # Revert dynamic switching: ensure button always has the right icon if needed
    if not enabled:
         # Ensure we are back to symbolic if we were in pitch black
         image = window.add_btn.get_image()
         if isinstance(image, Gtk.Image):
              image.set_from_icon_name("list-add-symbolic", Gtk.IconSize.BUTTON)
         else:
              window.add_btn.set_image(Gtk.Image.new_from_icon_name("list-add-symbolic", Gtk.IconSize.BUTTON))

    screen = Gdk.Screen.get_default()
    if enabled:
        Gtk.StyleContext.add_provider_for_screen(
            screen, window.pitch_black_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION + 1
        )
    else:
        Gtk.StyleContext.remove_provider_for_screen(
            screen, window.pitch_black_provider
        )
