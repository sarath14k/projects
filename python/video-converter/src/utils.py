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
    label, entry, textview { font-family: "Inter", "Roboto", "Segoe UI", "Cantarell", "Ubuntu", sans-serif; }
    .dim-label { opacity: 0.8; font-size: 11px; margin-bottom: 2px; font-weight: 600; letter-spacing: 0.5px; }
    .sidebar-bg { background-color: alpha(currentColor, 0.03); border-right: 1px solid alpha(currentColor, 0.1); }
    .row-card { border-radius: 12px; border: 1px solid alpha(currentColor, 0.08); background-color: alpha(currentColor, 0.03); padding: 8px; }
    .file-list { background: transparent; }
    .file-list row { padding-bottom: 8px; background: transparent; }
    .file-list row:last-child { padding-bottom: 0; }
    .file-list row:hover { background: transparent; }
    .active-row .row-card { border: 1px solid #2ec27e; background-color: alpha(#2ec27e, 0.08); }
    .thumbnail { border-radius: 8px; background-color: #000000; }
    .drag-active { border: 2px dashed #2ec27e; background-color: alpha(#2ec27e, 0.1); }
    .destructive-action { background-image: none; background-color: #e74c3c; color: white; }
    .flat-button { min-height: 24px; min-width: 24px; padding: 0px; margin: 0px; border: none; background: transparent; box-shadow: none; color: alpha(currentColor, 0.5); }
    .flat-button:hover { background-color: alpha(currentColor, 0.1); color: #2ec27e; }
    .flat-button:active { background-color: alpha(currentColor, 0.2); }
    .suggested-action { background-image: none; background-color: #2ec27e; color: #000000; font-weight: bold; border: none; border-radius: 4px; padding: 4px 8px; }
    .suggested-action label { background-color: transparent; color: inherit; }
    .suggested-action:hover { background-color: #3ad68e; }
    .suggested-action:disabled { background-color: alpha(currentColor, 0.1); color: alpha(currentColor, 0.5); }
    .row-card:hover { background-color: alpha(currentColor, 0.08); transition: background-color 0.2s ease; }
    .row-remove-btn:hover { color: #ff5555; background-color: alpha(#ff5555, 0.1); border-radius: 4px; }
    progressbar trough { min-height: 8px; border-radius: 4px; background-color: alpha(currentColor, 0.1); }
    progressbar progress { min-height: 8px; border-radius: 4px; }
    .success-bar progress { background-color: #2ec27e; }
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
