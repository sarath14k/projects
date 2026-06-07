#!/usr/bin/env python3
import os
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.insert(0, str(root_dir))

os.environ["GDK_BACKEND"] = "wayland,x11"

import gi

# Strict Version Check
try:
    gi.require_version("Gtk", "3.0")
    gi.require_version("Gdk", "3.0")
    gi.require_version("GdkPixbuf", "2.0")
except ValueError as e:
    print(f"Error: Missing required GTK3 libraries. {e}")
    sys.exit(1)

from gi.repository import Gtk

from src.ui import VideoConverter

from src.utils import check_dependencies

if __name__ == "__main__":
    check_dependencies()
    app = VideoConverter()
    app.show_all()
    
    if len(sys.argv) > 1:
        paths_to_add = []
        for arg in sys.argv[1:]:
            p = Path(arg).resolve()
            if p.exists() and p.is_file():
                paths_to_add.append(str(p))
        if paths_to_add:
            # Load files in a idle callback to ensure GTK is ready
            GLib.idle_add(lambda: app.file_manager.add_files(paths_to_add) and False)
            
    Gtk.main()
