import os
import shutil
import subprocess
import sys

from gi.repository import GLib

from concurrent.futures import ThreadPoolExecutor
from .config import APP_NAME, CACHE_DIR


THUMB_POOL = ThreadPoolExecutor(max_workers=4)


def ui(fn, *args):
    """Safe wrapper to run UI updates from threads."""
    GLib.idle_add(fn, *args)


def get_package_manager():
    """Detects the system package manager."""
    if shutil.which("apt-get"):
        return "apt"
    elif shutil.which("pacman"):
        return "pacman"
    elif shutil.which("dnf"):
        return "dnf"
    return None


def check_dependencies():
    """Checks for binary dependencies and installs them if missing."""
    # Map internal names to package names for different distros
    # Format: "binary_name": {"apt": "pkg_name", "pacman": "pkg_name"}
    dependency_map = {
        "ffmpeg": {"apt": "ffmpeg", "pacman": "ffmpeg", "dnf": "ffmpeg"},
        "ffprobe": {"apt": "ffmpeg", "pacman": "ffmpeg", "dnf": "ffmpeg"},
        "trash-put": {"apt": "trash-cli", "pacman": "trash-cli", "dnf": "trash-cli"},
    }

    missing_pkgs = set()
    manager = get_package_manager()

    for bin_name, pkg_map in dependency_map.items():
        if shutil.which(bin_name) is None:
            if manager and manager in pkg_map:
                missing_pkgs.add(pkg_map[manager])
            else:
                print(
                    f"Warning: Missing dependency '{bin_name}'. Please install it manually."
                )

    if missing_pkgs and manager:
        print(f"Missing packages detected: {', '.join(missing_pkgs)}")
        try:
            cmd = []
            if manager == "apt":
                # Ubuntu/Debian requires updating cache sometimes, but we'll try direct install
                cmd = ["pkexec", "apt-get", "install", "-y"] + list(missing_pkgs)
            elif manager == "pacman":
                cmd = ["pkexec", "pacman", "-S", "--needed", "--noconfirm"] + list(
                    missing_pkgs
                )
            elif manager == "dnf":
                cmd = ["pkexec", "dnf", "install", "-y"] + list(missing_pkgs)

            if cmd:
                subprocess.check_call(cmd)
        except subprocess.CalledProcessError:
            print("Failed to install dependencies. Please install them manually.")
            sys.exit(1)

    if shutil.which("udevadm") is None:
        print("Warning: 'udevadm' missing.")

    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        for f in CACHE_DIR.glob("*.jpg"):
            try:
                f.unlink()
            except:
                pass
    except:
        pass


def load_static_css():
    from gi.repository import Gdk, Gtk

    css = """
    @define-color bg_color #242424;
    @define-color fg_color #eeeeee;
    @define-color card_bg #323232;
    @define-color accent_color #2ec27e;
    @define-color accent_hover #3ad68e;
    @define-color destructive_color #e74c3c;
    @define-color destructive_hover #ff6b6b;

    * {
        font-family: "Inter", "Roboto", "Segoe UI", "Cantarell", "Ubuntu", sans-serif;
    }

    window, textview, .background {
        background-color: @bg_color;
        color: @fg_color;
    }

    .dim-label { 
        opacity: 0.6; 
        font-size: 11px; 
        margin-bottom: 2px; 
        font-weight: 600; 
        letter-spacing: 0.5px; 
    }

    .sidebar-bg { 
        background-color: alpha(#000000, 0.1); 
        border-right: 1px solid alpha(#ffffff, 0.05); 
    }

    .row-card { 
        border-radius: 16px; 
        border: 1px solid alpha(#ffffff, 0.05); 
        background-color: @card_bg; 
        padding: 12px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    
    .row-card:hover { 
        background-color: shade(@card_bg, 1.05); 
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        transition: all 0.2s ease; 
    }

    .file-list { background: transparent; }
    .file-list row { 
        padding-bottom: 12px; 
        background: transparent; 
        margin-left: 4px;
        margin-right: 4px;
    }
    .file-list row:last-child { padding-bottom: 0; }
    .file-list row:hover { background: transparent; }

    .active-row .row-card { 
        border: 1px solid @accent_color; 
        background-color: alpha(@accent_color, 0.08); 
    }

    .thumbnail { 
        border-radius: 8px; 
        background-color: #000000; 
    }

    .drag-active { 
        border: 2px dashed @accent_color; 
        background-color: alpha(@accent_color, 0.1); 
        border-radius: 16px;
    }

    button {
        min-height: 38px;
        min-width: 38px;
        padding: 0 12px;
        border-radius: 8px;
        font-weight: 500;
        transition: background-color 0.15s ease;
    }

    .destructive-action { 
        background-image: none; 
        background-color: @destructive_color; 
        color: white; 
        border: none;
        min-height: 38px;
        min-width: 38px;
    }
    .destructive-action:hover { background-color: @destructive_hover; }

    .flat-button { 
        min-height: 28px; 
        min-width: 28px; 
        padding: 4px; 
        margin: 0px; 
        border: none; 
        background: transparent; 
        box-shadow: none; 
        color: alpha(@fg_color, 0.6); 
        border-radius: 50%;
    }
    .flat-button:hover { 
        background-color: alpha(@fg_color, 0.1); 
        color: @accent_color; 
    }
    .flat-button:active { background-color: alpha(@fg_color, 0.2); }

    .suggested-action { 
        background-image: none; 
        background-color: @accent_color; 
        color: #000000; 
        font-weight: 700; 
        border: none; 
        border-radius: 8px; 
        padding: 0 12px; 
        min-height: 38px;
        min-width: 38px;
    }
    .suggested-action label { background-color: transparent; color: inherit; }
    .suggested-action:hover { background-color: @accent_hover; }
    .suggested-action:disabled { 
        background-color: alpha(@fg_color, 0.1); 
        color: alpha(@fg_color, 0.4); 
    }

    .row-remove-btn { color: alpha(@fg_color, 0.5); }
    .row-remove-btn:hover { 
        color: @destructive_hover; 
        background-color: alpha(@destructive_color, 0.15); 
        border-radius: 50%; 
    }

    progressbar trough { 
        min-height: 6px; 
        border-radius: 3px; 
        background-color: alpha(#000000, 0.3); 
    }
    progressbar progress { 
        min-height: 6px; 
        border-radius: 3px; 
        background-color: @accent_color;
    }
    .success-bar progress { background-color: @accent_color; }
    """
    p = Gtk.CssProvider()
    p.load_from_data(css.encode("utf-8"))
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), p, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


class SleepInhibitor:
    def __init__(self):
        self._proc = None

    def start(self):
        if not self._proc:
            try:
                self._proc = subprocess.Popen(
                    [
                        "systemd-inhibit",
                        "--what=idle",
                        "--who=VideoConverter",
                        "--why=Encoding",
                        "sleep",
                        "infinity",
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except:
                pass

    def stop(self):
        if self._proc:
            self._proc.terminate()
            self._proc = None
