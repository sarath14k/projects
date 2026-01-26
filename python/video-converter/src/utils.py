import glob
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

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

def get_file_size(path):
    """Get file size in bytes."""
    try:
        return os.path.getsize(path)
    except:
        return 0

def human_readable_size(size_bytes):
    """Convert bytes to human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024**2:
        return f"{size_bytes / 1024:.1f}KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes / 1024**2:.1f}MB"
    elif size_bytes < 1024**4:
        return f"{size_bytes / 1024**3:.1f}GB"
    else:
        return f"{size_bytes / 1024**4:.1f}TB"

def open_folder_safe(path):
    """Open folder in file manager."""
    if not path or not os.path.exists(path):
        return
    managers = ["dolphin", "thunar", "nautilus", "nemo", "pcmanfm", "caja"]
    for fm in managers:
        if shutil.which(fm):
            subprocess.Popen([fm, path])
            return
    subprocess.Popen(["xdg-open", path])

def send_notification(title, body, app_name="Video Converter"):
    """Send desktop notification."""
    try:
        subprocess.run(["notify-send", "-a", app_name, title, body])
    except:
        pass

def format_time(sec):
    """Format seconds to HH:MM:SS or MM:SS."""
    m, s = divmod(int(sec), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def get_render_devices():
    """Get available GPU render devices."""
    devs = glob.glob("/dev/dri/renderD*")
    devs.sort()
    devices = []
    for d in devs:
        label = os.path.basename(d)
        try:
            u = subprocess.check_output(
                ["udevadm", "info", "--query=property", d], text=True
            )
            for line in u.split("\\n"):
                if "PCI_ID=" in line:
                    label += f" ({line.split('=')[1]})"
                    break
        except:
            pass
        devices.append((d, label))

    if not devices:
        devices.append(("/dev/dri/renderD128", "renderD128 (Default)"))

    devices.insert(0, ("cpu", "CPU Only"))
    return devices

def get_video_info(file_path):
    """Get video file metadata using ffprobe.

    Returns:
        tuple: (duration, fps, codec, bitrate, width)
    """
    try:
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "format=duration,bit_rate:stream=r_frame_rate,codec_name,width,bit_rate",
            "-of",
            "json",
            file_path,
        ]
        out = subprocess.check_output(cmd, timeout=2, text=True)
        data = json.loads(out)

        dur = float(data["format"].get("duration", 1.0))

        # Try format bit_rate first, then stream bit_rate
        src_bitrate = data["format"].get("bit_rate")
        if not src_bitrate and "streams" in data:
            src_bitrate = data["streams"][0].get("bit_rate")

        src_bitrate = float(src_bitrate) if src_bitrate else 5_000_000

        fps_str = data["streams"][0].get("r_frame_rate", "30/1")
        fps = (
            float(fps_str.split("/")[0]) / float(fps_str.split("/")[1])
            if "/" in fps_str
            else float(fps_str)
        )
        codec = data["streams"][0].get("codec_name", "unknown")
        width = int(data["streams"][0].get("width", 1920))

        return dur, fps, codec, src_bitrate, width
    except:
        return 1.0, 30.0, "unknown", 5_000_000, 1920

def generate_output_path(src_path, quality_map, quality_text, file_count_in_dir, output_dir_name="Converted"):
    """Generate output path for converted video. Always uses output folder."""
    src = Path(src_path)
    val = quality_map.get(quality_text, 26)
    suffix = f"preset{val}" if val < 13 else f"qvbr{val}"
    src_dir = src.parent

    # Always create and use output folder
    out_dir = src_dir / output_dir_name
    out_dir.mkdir(exist_ok=True)

    return str(out_dir / f"{src.stem}_comp_{suffix}.mkv"), str(out_dir)
