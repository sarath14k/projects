from gi.repository import Gtk, Gdk

def build_queue(window):
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    
    header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    header.get_style_context().add_class("sidebar-header")
    header.pack_start(Gtk.Label(label="Conversion Queue"), False, False, 0)
    box.pack_start(header, False, False, 0)
    
    # Root container for list and empty state
    stack = Gtk.Overlay()
    box.pack_start(stack, True, True, 0)
    
    # 1. Scrolled List
    scrolled = Gtk.ScrolledWindow()
    scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    stack.add(scrolled)
    
    window.file_list = Gtk.ListBox()
    window.file_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
    window.file_list.connect("row-selected", window.on_row_selected)
    scrolled.add(window.file_list)
    
    # --- Drag and Drop Setup ---
    # Register "row" as a reorder target and "text/uri-list" for system drops
    targets = [
        Gtk.TargetEntry.new("row", Gtk.TargetFlags.SAME_APP, 1),
        Gtk.TargetEntry.new("text/uri-list", 0, 0)
    ]
    
    # Enable reordering source
    window.file_list.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [targets[0]], Gdk.DragAction.MOVE)
    window.file_list.connect("drag-data-get", window.file_manager.on_drag_data_get)

    # Enable drop destination
    window.file_list.drag_dest_set(Gtk.DestDefaults.ALL, targets, Gdk.DragAction.MOVE | Gdk.DragAction.COPY)
    
    # Connect signals
    window.file_list.connect("drag-data-received", window.file_manager.on_drag_data_received)
    window.file_list.connect("drag-motion", window.file_manager.on_drag_motion)
    window.file_list.connect("drag-leave", window.file_manager.on_drag_leave)
    
    # 2. Empty State / Drop Zone
    window.empty_zone = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    window.empty_zone.set_valign(Gtk.Align.CENTER)
    window.empty_zone.set_halign(Gtk.Align.CENTER)
    window.empty_zone.get_style_context().add_class("drop-zone")
    
    drop_icon = Gtk.Image.new_from_icon_name("document-send-symbolic", Gtk.IconSize.DIALOG)
    drop_icon.set_pixel_size(64)
    drop_icon.set_opacity(0.3)
    window.empty_zone.pack_start(drop_icon, False, False, 0)
    
    drop_lbl = Gtk.Label()
    drop_lbl.set_markup("<span size='large' weight='bold' alpha='40%'>Drop Videos Here</span>")
    window.empty_zone.pack_start(drop_lbl, False, False, 0)
    
    drop_sub = Gtk.Label(label="Or click the '+' button to begin")
    drop_sub.get_style_context().add_class("dim-label")
    window.empty_zone.pack_start(drop_sub, False, False, 0)
    
    stack.add_overlay(window.empty_zone)
    window.empty_label = window.empty_zone
    
    # Enable drops on empty zone too (must accept URIs)
    window.empty_zone.drag_dest_set(Gtk.DestDefaults.ALL, [targets[1]], Gdk.DragAction.COPY)
    window.empty_zone.connect("drag-data-received", window.file_manager.on_drag_data_received)
    window.empty_zone.connect("drag-motion", window.file_manager.on_drag_motion)
    window.empty_zone.connect("drag-leave", window.file_manager.on_drag_leave)
    
    return box
