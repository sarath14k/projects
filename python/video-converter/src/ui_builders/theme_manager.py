"""Theme manager for handling dynamic theme switching from the registry."""

from gi.repository import Gtk, Gdk
from ..css import BASE_CSS
from ..themes import THEMES

def apply_theme(theme_name):
    """Apply a theme by name from the registry."""
    theme = THEMES.get(theme_name)
    if not theme:
        return

    # Generate CSS from template
    css_data = BASE_CSS.format(
        bg_color=theme.bg_color,
        fg_color=theme.fg_color,
        card_bg=theme.card_bg,
        accent_color=theme.accent_color,
        accent_hover=theme.accent_hover,
        destructive_color=theme.destructive_color,
        destructive_hover=theme.destructive_hover,
        warning_color=theme.warning_color,
        warning_hover=theme.warning_hover,
        success_color=theme.success_color,
        info_color=theme.info_color,
        border_color=theme.border_color,
        shadow_color=theme.shadow_color
    )

    provider = Gtk.CssProvider()
    provider.load_from_data(css_data.encode("utf-8"))
    
    screen = Gdk.Screen.get_default()
    Gtk.StyleContext.add_provider_for_screen(
        screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    
    # Store for reference
    return provider

def init_theme(window):
    """Initialize theme on window startup."""
    theme_name = window.config.get("theme", "Modern (System)")
    window.css_provider = apply_theme(theme_name)
    
    # Update GTK settings to prefer dark if it's a dark theme
    settings = Gtk.Settings.get_default()
    settings.set_property("gtk-application-prefer-dark-theme", True)
    settings.set_property("gtk-theme-name", "Adwaita-dark")

def on_theme_changed(combo, window):
    """Handle theme selection from ComboBox."""
    theme_name = combo.get_active_text()
    if theme_name:
        window.css_provider = apply_theme(theme_name)
        window.config["theme"] = theme_name
        # Simple feedback
        if hasattr(window, 'queue_status'):
             window.queue_status.set_markup(f"<span foreground='{THEMES[theme_name].accent_color}'>Theme updated to {theme_name}</span>")
