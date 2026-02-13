"""Header area builder for the video converter UI."""

from gi.repository import Gtk, Gdk

def build_header(window):
    """Build and configure the header areas (standard and compact).

    Args:
        window: The main VideoConverter window instance
    """
    # 1. Standard Header (Gtk.HeaderBar)
    window.header_bar = Gtk.HeaderBar()
    window.header_bar.set_show_close_button(True)
    window.header_bar.set_has_subtitle(False)
    window.header_bar.props.title = "Video Converter"

    # Theme Selector for Standard Mode
    from ..themes import THEMES
    from . import theme_manager

    window.theme_combo = Gtk.ComboBoxText()
    for theme_name in THEMES.keys():
        window.theme_combo.append_text(theme_name)
    
    current_theme = window.config.get("theme", "Modern (System)")
    model = window.theme_combo.get_model()
    for i, row in enumerate(model):
        if row[0] == current_theme:
            window.theme_combo.set_active(i)
            break
            
    window.theme_combo.connect("changed", theme_manager.on_theme_changed, window)
    window.header_bar.pack_end(window.theme_combo)

    # 2. Compact/Stacked Header (Gtk.Box inside vbox)
    window.header_stacked = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    window.header_stacked.get_style_context().add_class("header-area")
    window.header_stacked.get_style_context().add_class("compact-header")
    
    row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    row1.get_style_context().add_class("header-row")
    title_lbl = Gtk.Label()
    title_lbl.set_markup("<span weight='bold'>Video Converter</span>")
    title_lbl.set_xalign(0)
    row1.pack_start(title_lbl, True, True, 0)
    
    close_btn = Gtk.Button.new_from_icon_name("window-close-symbolic", Gtk.IconSize.MENU)
    close_btn.get_style_context().add_class("flat-button")
    close_btn.connect("clicked", lambda _: window.close())
    row1.pack_end(close_btn, False, False, 0)
    
    window.header_stacked.pack_start(row1, False, False, 0)
    
    # We'll move the theme_combo between header_bar and header_stacked as needed
    window.header_compact_row2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    window.header_stacked.pack_start(window.header_compact_row2, False, False, 0)

    # Initial packing (standard mode)
    window.set_titlebar(window.header_bar)
    window.vbox.pack_start(window.header_stacked, False, False, 0)
    window.header_stacked.hide()
    
    # Check initial state
    update_header_layout(window)

def update_header_layout(window):
    """Switch header between HeaderBar and stacked Box."""
    is_compact = hasattr(window, "is_compact") and window.is_compact
    
    # Remove theme combo from current parent
    parent = window.theme_combo.get_parent()
    if parent:
        parent.remove(window.theme_combo)

    if is_compact:
        # Use stacked layout
        window.set_titlebar(None) # Use undecorated-like look by removing titlebar
        window.header_bar.hide()
        window.header_stacked.show()
        window.header_compact_row2.pack_start(window.theme_combo, True, True, 0)
        window.theme_combo.show()
    else:
        # Use standard HeaderBar
        window.set_titlebar(window.header_bar)
        window.header_bar.show()
        window.header_stacked.hide()
        window.header_bar.pack_end(window.theme_combo)
        window.theme_combo.show()

    window.header_bar.show_all()
    window.header_stacked.show_all()
    if not is_compact:
        window.header_stacked.hide()
