from gi.repository import Gtk, Gdk
from ..components.file_row import FileRow
from ..utils import ui

class FileManager:
    def __init__(self, window):
        self.window = window
        self.files = {} # path -> FileRow

    def add_files(self, paths):
        for p in paths:
            if p not in self.files:
                row = FileRow(
                    p, 
                    self.remove_file
                )
                self.window.file_list_box.add(row.root)
                self.files[p] = row
                
                # Check output conflict
                from pathlib import Path
                out_path = Path(self.window._get_out_path(p))
                if out_path.exists():
                    row.show_conflict()

        self.window.file_list_box.show_all()
        self.window._update_empty_state()
        self.window.start_btn.set_sensitive(bool(self.files))
        self.window.open_out_btn.set_sensitive(bool(self.files))

    def remove_file(self, path):
        if path in self.files:
            row = self.files[path]
            # Since root is inside a ListBoxRow (added automatically by Gtk.ListBox.add)
            # we need to find that row container to remove it.
            row_container = row.root.get_parent()
            self.window.file_list_box.remove(row_container)
            del self.files[path]
            self.window._update_empty_state()
            self.window.start_btn.set_sensitive(bool(self.files))
            self.window.open_out_btn.set_sensitive(bool(self.files))

    def clear_all(self):
        # Get the currently encoding file ID from conversion_manager if any
        current_id = None
        if hasattr(self.window, "conversion_manager") and self.window.conversion_manager.current_file_row:
            current_id = self.window.conversion_manager.current_file_row.id
        
        # Remove all files except the currently encoding one
        files_to_remove = [fid for fid in self.files.keys() if fid != current_id]
        for fid in files_to_remove:
            row = self.files[fid]
            row_container = row.root.get_parent()
            self.window.file_list_box.remove(row_container)
            del self.files[fid]
        
        # If the list is truly empty (nothing was encoding), clear status labels
        if not self.files:
            self.window.queue_status.set_markup("Ready.")
        
        self.window._update_empty_state()
        self.window.start_btn.set_sensitive(bool(self.files))
        self.window.open_out_btn.set_sensitive(bool(self.files))

    def on_drag_motion(self, listbox, context, x, y, time):
        # Determine if we are dragging a row (reorder) or URIs (adding files)
        target = listbox.drag_dest_find_target(context, None)
        is_row = (target and target.name() == "row")
        
        # Highlight target row only for reordering
        if is_row:
            row_container = listbox.get_row_at_y(y)
            if row_container:
                listbox.drag_highlight_row(row_container)
            Gdk.drag_status(context, Gdk.DragAction.MOVE, time)
        else:
            # File drop from outside
            listbox.drag_unhighlight()
            Gdk.drag_status(context, Gdk.DragAction.COPY, time)
            
        return True

    def on_drag_data_received(self, listbox, context, x, y, data, info, time):
        # Handle file drops (text/uri-list)
        if info == 1:
            self.window.on_drag_data_received(listbox, context, x, y, data, info, time)
            return

        # Handle reordering (row)
        dragged_id = data.get_data().decode()
        if dragged_id not in self.files:
            Gtk.drag_finish(context, False, False, time)
            return

        # Find where to drop
        target_row = listbox.get_row_at_y(y)
        if not target_row:
            Gtk.drag_finish(context, False, False, time)
            return

        dragged_row = self.files[dragged_id].root.get_parent()
        target_index = target_row.get_index()
        
        # Move the row container
        listbox.remove(dragged_row)
        listbox.insert(dragged_row, target_index)
        
        Gtk.drag_finish(context, True, False, time)

    def get_file_list(self):
        # Return file rows in the order they appear in the Gtk.ListBox
        ordered_files = []
        for row_container in self.window.file_list_box.get_children():
            # The FileRow.root (frame) is the child of the ListBoxRow
            frame = row_container.get_child()
            # We need to find which FileRow object matches this frame
            for f_row in self.files.values():
                if f_row.root == frame:
                    ordered_files.append(f_row)
                    break
        return ordered_files
