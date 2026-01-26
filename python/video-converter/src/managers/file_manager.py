from gi.repository import Gtk, Gdk, GLib
import os
from ..components.file_row import FileRow
from ..utils import ui
from ..config import VIDEO_EXTS

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
                from ..config import OUTPUT_DIR_NAME, QUALITY_MAP_GPU
                from .. import utils

                # Use current UI state for quality
                q_map = self.window.active_quality_map if hasattr(self.window, "active_quality_map") else QUALITY_MAP_GPU
                q_text = self.window.quality.get_active_text() if hasattr(self.window, "quality") else "Main - 50% (QV-26)"

                out_path_str, _ = utils.generate_output_path(
                    p, q_map, q_text, len(paths), OUTPUT_DIR_NAME
                )
                if Path(out_path_str).exists():
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

    def sort_alphabetically(self):
        """Sort the queue alphabetically by filename."""
        if not self.files:
            return

        # Get sorted list of file paths by filename
        from pathlib import Path
        sorted_paths = sorted(self.files.keys(), key=lambda p: Path(p).name.lower())

        # Reorder rows in the listbox
        for i, path in enumerate(sorted_paths):
            row = self.files[path]
            row_container = row.root.get_parent()
            self.window.file_list_box.remove(row_container)
            self.window.file_list_box.insert(row_container, i)

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

    def process_dropped_data(self, data):
        """Process dropped data (URIs) and add valid video files."""
        uris = data.get_uris()
        paths = []
        from pathlib import Path
        for uri in uris:
            try:
                path_str, _ = GLib.filename_from_uri(uri)
                path = Path(path_str)
                if path.is_file() and path.suffix.lower() in VIDEO_EXTS:
                    # Skip already converted files
                    if "_comp_" not in path.name and "Converted" not in str(path):
                        paths.append(str(path))
                elif path.is_dir():
                    for root, _, files in os.walk(path):
                        # Skip Converted folders
                        if "Converted" in root:
                            continue
                        for name in files:
                            sub_path = Path(root) / name
                            if sub_path.suffix.lower() in VIDEO_EXTS and "_comp_" not in name:
                                paths.append(str(sub_path))
            except Exception as e:
                print(f"Error processing drag URI {uri}: {e}")
                continue
        if paths:
            self.add_files(paths)

    def on_drag_data_received(self, listbox, context, x, y, data, info, time):
        # Handle file drops (text/uri-list)
        if info == 1:
            self.process_dropped_data(data)
            Gtk.drag_finish(context, True, False, time)
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
