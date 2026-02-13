from gi.repository import Gtk, Gdk, GLib
import os
import uuid
from pathlib import Path
from ..components.file_row import FileRow
from ..utils import ui
from .. import utils
from ..config import MEDIA_EXTS, OUTPUT_DIR_NAME, QUALITY_MAP_GPU

class FileManager:
    def __init__(self, window):
        self.window = window
        self.files = {} # id -> FileRow
        self.order = [] # list of ids

    def add_files(self, paths):
        params = self._get_current_params()
        for p in paths:
            # Filter out already converted files or files in output directory
            if "_comp_" in os.path.basename(p) or OUTPUT_DIR_NAME in p:
                continue

            row_id = str(uuid.uuid4())
            row = FileRow(
                p,
                self.remove_file,
                params=params.copy(),
                row_id=row_id
            )
            self.window.file_list_box.add(row.root)
            self.files[row_id] = row
            self.order.append(row_id)

            # Check output conflict

            # Use current UI state for quality
            q_map = self.window.active_quality_map if hasattr(self.window, "active_quality_map") else QUALITY_MAP_GPU
            q_text = self.window.quality.get_active_text() if hasattr(self.window, "quality") else "Main - 50% (QV-26)"

            out_path_str, _ = utils.generate_output_path(
                p, 
                q_map, 
                q_text, 
                len(paths), 
                OUTPUT_DIR_NAME,
                codec_key=params["codec_key"],
                audio_codec_key=params["audio_codec"]
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
            if path in self.order:
                self.order.remove(path)
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
            if fid in self.order:
                self.order.remove(fid)

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
        
        self.order = sorted_paths

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
        for uri in uris:
            try:
                path_str, _ = GLib.filename_from_uri(uri)
                path = Path(path_str)
                if path.is_file() and path.suffix.lower() in MEDIA_EXTS:
                    # Skip already converted files or folders
                    if "_comp_" not in path.name and OUTPUT_DIR_NAME not in str(path):
                        paths.append(str(path))
                elif path.is_dir():
                    for root, _, files in os.walk(path):
                        # Skip Converted folders
                        if OUTPUT_DIR_NAME in root:
                            continue
                        for name in files:
                            sub_path = Path(root) / name
                            if (
                                sub_path.suffix.lower() in MEDIA_EXTS
                                and "_comp_" not in name
                            ):
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

        # Update internal order
        if dragged_id in self.order:
            self.order.remove(dragged_id)
        self.order.insert(target_index, dragged_id)

        Gtk.drag_finish(context, True, False, time)

    def get_file_list(self):
        """Return file rows in the current order."""
        return [self.files[fid] for fid in self.order if fid in self.files]

    def apply_settings_to_all(self):
        """Apply current sidebar settings to all files in the queue."""
        params = self._get_current_params()
        for row in self.files.values():
            row.params.update(params)
            # Check for conflict with new settings
            q_map = (
                self.window.active_quality_map
                if hasattr(self.window, "active_quality_map")
                else QUALITY_MAP_GPU
            )
            # Note: generate_output_path now needs more params
            from ..utils import generate_output_path

            out_path, _ = generate_output_path(
                row.path,
                q_map,
                params["quality_text"],
                len(self.files),
                process_mode=params["process_mode"],
                codec_key=params["codec_key"],
                audio_codec_key=params["audio_codec"],
            )
            if Path(out_path).exists():
                row.show_conflict()
            else:
                row.conflict.hide()

        self.window.queue_status.set_text("Settings applied to all.")

    def _get_current_params(self):
        """Extract current settings from the sidebar UI."""
        return {
            "gpu": self.window.gpu_device.get_active_id(),
            "codec_key": self.window.codec.get_active_text(),
            "quality_text": self.window.quality.get_active_text(),
            "scale": self.window.scale_chk.get_active(),
            "process_mode": self.window.process_mode.get_active_text(),
            "audio_codec": self.window.audio_codec.get_active_text(),
        }
