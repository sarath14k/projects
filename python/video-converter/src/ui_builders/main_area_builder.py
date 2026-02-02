"""Main area builder for file list and controls."""

from gi.repository import Gtk, Gdk, Pango
from ..config import MEDIA_EXTS

def build_main_area(window):
    """Build the main file list area with controls.

    Args:
        window: The main VideoConverter window instance
    """
    # Get main_hbox from window
    main_hbox = window.main_hbox

    right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    main_hbox.pack_start(right_box, True, True, 0)

    # Top controls
    top_controls = Gtk.Box(spacing=16)
    top_controls.set_border_width(20)
    top_controls.set_margin_bottom(0)
    right_box.pack_start(top_controls, False, False, 0)

    # Open output folder button
    window.open_out_btn = Gtk.Button.new_from_icon_name(
        "folder-open-symbolic", Gtk.IconSize.BUTTON
    )
    window.open_out_btn.set_sensitive(False)
    window.open_out_btn.set_tooltip_text("Open Output Folder")
    window.open_out_btn.connect("clicked", window.open_output_folder)
    top_controls.pack_start(window.open_out_btn, False, False, 0)

    # Add files button
    window.add_btn = Gtk.Button.new_from_icon_name(
        "list-add-symbolic", Gtk.IconSize.BUTTON
    )
    window.add_btn.get_style_context().add_class("suggested-action")
    window.add_btn.set_tooltip_text("Add Videos")
    window.add_btn.connect("clicked", window.pick_files)
    top_controls.pack_start(window.add_btn, False, False, 0)

    # Sort button (alphabetical)
    sort_btn = Gtk.Button.new_from_icon_name(
        "view-sort-ascending-symbolic", Gtk.IconSize.BUTTON
    )
    sort_btn.set_tooltip_text("Sort A-Z")
    sort_btn.connect("clicked", lambda _: window.file_manager.sort_alphabetically())
    top_controls.pack_start(sort_btn, False, False, 0)

    # Clear button
    clear_btn = Gtk.Button.new_from_icon_name(
        "edit-clear-all-symbolic", Gtk.IconSize.BUTTON
    )
    clear_btn.set_tooltip_text("Clear List")
    clear_btn.connect("clicked", lambda _: window.file_manager.clear_all())
    top_controls.pack_end(clear_btn, False, False, 0)

    right_box.pack_start(
        Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0
    )

    # Stack for empty state / file list
    window.stack = Gtk.Stack()
    window.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
    right_box.pack_start(window.stack, True, True, 0)

    # Empty state
    window.empty_state = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    window.empty_state.set_valign(Gtk.Align.CENTER)
    window.empty_state.set_halign(Gtk.Align.CENTER)
    icon = Gtk.Image.new_from_icon_name(
        "video-x-generic-symbolic", Gtk.IconSize.DIALOG
    )
    icon.set_pixel_size(96)
    icon.set_opacity(0.3)
    lbl = Gtk.Label()
    lbl.set_markup(
        "<span size='xx-large' weight='bold' foreground='#555555'>Drop Videos Here</span>"
    )
    window.empty_state.pack_start(icon, False, False, 0)
    window.empty_state.pack_start(lbl, False, False, 0)
    window.stack.add_named(window.empty_state, "empty")

    # File list
    list_scroll = Gtk.ScrolledWindow()
    list_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

    window.file_list_box = Gtk.ListBox()
    window.file_list_box.set_selection_mode(Gtk.SelectionMode.NONE)
    window.file_list_box.get_style_context().add_class("file-list")

    # Drag-and-drop for reordering AND adding files
    window.file_list_box.drag_dest_set(
        Gtk.DestDefaults.ALL,
        [
            Gtk.TargetEntry.new("row", Gtk.TargetFlags.SAME_APP, 0),
            Gtk.TargetEntry.new("text/uri-list", 0, 1)
        ],
        Gdk.DragAction.MOVE | Gdk.DragAction.COPY
    )
    window.file_list_box.connect("drag-motion", lambda *a: window.file_manager.on_drag_motion(*a))
    window.file_list_box.connect("drag-data-received", lambda *a: window.file_manager.on_drag_data_received(*a))

    list_scroll.add(window.file_list_box)
    window.stack.add_named(list_scroll, "list")

    # Bottom controls
    controls_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
    controls_area.get_style_context().add_class("bottom-bar")
    controls_area.set_border_width(20)
    right_box.pack_end(controls_area, False, False, 0)
    right_box.pack_end(
        Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0
    )

    # Queue status label
    window.queue_status = Gtk.Label(label="Ready.")
    window.queue_status.set_use_markup(True)
    window.queue_status.set_justify(Gtk.Justification.LEFT)
    window.queue_status.set_xalign(0)
    window.queue_status.set_ellipsize(Pango.EllipsizeMode.END)
    window.queue_status.set_max_width_chars(30)
    controls_area.pack_start(window.queue_status, True, True, 0)

    # Start button
    window.start_btn = Gtk.Button.new_from_icon_name(
        "media-playback-start-symbolic", Gtk.IconSize.BUTTON
    )
    window.start_btn.get_style_context().add_class("suggested-action")
    window.start_btn.set_tooltip_text("Start Queue")
    window.start_btn.set_valign(Gtk.Align.CENTER)
    window.start_btn.connect("clicked", lambda _: window.conversion_manager.start_encoding())
    controls_area.pack_end(window.start_btn, False, False, 0)

    # Pause button
    window.pause_btn = Gtk.Button.new_from_icon_name(
        "media-playback-pause-symbolic", Gtk.IconSize.BUTTON
    )
    window.pause_btn.set_sensitive(False)
    window.pause_btn.set_tooltip_text("Pause")
    window.pause_btn.set_valign(Gtk.Align.CENTER)
    window.pause_btn.connect("clicked", lambda _: window.conversion_manager.pause_resume())
    controls_area.pack_end(window.pause_btn, False, False, 0)

    # Stop button
    window.stop_btn = Gtk.Button.new_from_icon_name(
        "media-playback-stop-symbolic", Gtk.IconSize.BUTTON
    )
    window.stop_btn.get_style_context().add_class("destructive-action")
    window.stop_btn.set_tooltip_text("Stop Queue")
    window.stop_btn.set_valign(Gtk.Align.CENTER)
    window.stop_btn.connect("clicked", lambda _: window.conversion_manager.stop_encoding())
    controls_area.pack_end(window.stop_btn, False, False, 0)
