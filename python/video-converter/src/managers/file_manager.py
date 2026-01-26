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
                    self.remove_file, 
                    self.move_row_up, 
                    self.move_row_down
                )
                self.window.file_list_box.add(row.root)
                self.files[p] = row
                
                # Check output conflict
                out_path = self.window._get_out_path(p)
                if out_path.exists():
                    row.show_conflict()

        self.window.file_list_box.show_all()
        self.window._update_empty_state()
        self.window.start_btn.set_sensitive(bool(self.files))
        self.window.open_out_btn.set_sensitive(bool(self.files))

    def remove_file(self, path):
        if path in self.files:
            row = self.files[path]
            self.window.file_list_box.remove(row.root)
            del self.files[path]
            self.window._update_empty_state()
            self.window.start_btn.set_sensitive(bool(self.files))
            self.window.open_out_btn.set_sensitive(bool(self.files))

    def clear_all(self):
        for row in self.files.values():
            self.window.file_list_box.remove(row.root)
        self.files.clear()
        self.window._update_empty_state()
        self.window.start_btn.set_sensitive(False)
        self.window.open_out_btn.set_sensitive(False)

    def move_row_up(self, file_id):
        keys = list(self.files.keys())
        try:
            idx = keys.index(file_id)
            if idx > 0:
                self.swap_rows(keys[idx], keys[idx - 1])
        except ValueError:
            pass

    def move_row_down(self, file_id):
        keys = list(self.files.keys())
        try:
            idx = keys.index(file_id)
            if idx < len(keys) - 1:
                self.swap_rows(keys[idx], keys[idx + 1])
        except ValueError:
            pass

    def swap_rows(self, id1, id2):
        row1 = self.files[id1].root
        row2 = self.files[id2].root
        
        # We need to reorder the keys in self.files dictionary to match visual order
        # Python 3.7+ dicts preserve insertion order.
        # This is a bit tricky with dicts. Ideally we should use a list of objects.
        # But for listbox reordering:
        
        parent = row1.get_parent()
        idx1 = row1.get_index()
        idx2 = row2.get_index()
        
        # Swap in UI
        # GtkListBox rows are ordered by index.
        # To swap, we can just remove and insert? Or use set_sort_func? 
        # Standard Gtk way is usually just reordering the widget children.
        
        # Actually simplest way for small lists:
        # parent.reorder_child(row1, idx2)
        # parent.reorder_child(row2, idx1)
        # Note: changing one index affects the other if not careful.
        
        target_idx = idx2 if idx1 < idx2 else idx2
        # If we move row1 to row2's position...
        
        # Let's just swap references in a list if we had one.
        # Since self.files is a dict, iteration order matters for processing?
        # Yes, encode_all iterates self.files.
        
        # We must reconstruct the dict in the new order.
        keys = list(self.files.keys())
        i1, i2 = keys.index(id1), keys.index(id2)
        keys[i1], keys[i2] = keys[i2], keys[i1]
        
        new_files = {k: self.files[k] for k in keys}
        self.files = new_files
        
        # Update UI
        parent = row1.get_parent() 
        # parent is the ListBox
        
        # To visually swap:
        # If moving UP: row1 is at i, want it at i-1. row2 is at i-1.
        # If moving DOWN: row1 is at i,, want it at i+1. row2 is at i+1.
        
        if idx1 < idx2:
            # Moving down
            parent.reorder_child(row1, idx2)
        else:
            # Moving up
            parent.reorder_child(row1, idx2)

    def get_file_list(self):
        return list(self.files.values())
