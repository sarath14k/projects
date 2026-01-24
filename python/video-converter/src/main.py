#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# ─── PATH FIX ───
# Allow importing 'src' modules when running this script directly
# We add the parent directory (video-converter/) to the system path
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.insert(0, str(root_dir))

# ─── FORCE BACKEND ───
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

# Now these imports will work correctly
from src.utils import check_dependencies

if __name__ == "__main__":
    check_dependencies()
    app = VideoConverter()
    app.show_all()
    Gtk.main()
