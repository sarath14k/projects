"""Helper utilities for file operations, system functions, and video metadata."""

import glob
import json
import os
import shutil
import subprocess
from pathlib import Path


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
            for line in u.split("\n"):
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
            "format=duration,bit_rate:stream=r_frame_rate,codec_name,width",
            "-of",
            "json",
            file_path,
        ]
        out = subprocess.check_output(cmd, timeout=2, text=True)
        data = json.loads(out)

        dur = float(data["format"].get("duration", 1.0))
        src_bitrate = float(data["format"].get("bit_rate", 5_000_000))

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
    """Generate output path for converted video.
    
    Args:
        src_path: Source file path
        quality_map: Quality mapping dict
        quality_text: Selected quality text
        file_count_in_dir: Number of files in same directory
        output_dir_name: Name of output subdirectory
        
    Returns:
        str: Output file path
    """
    src = Path(src_path)
    val = quality_map.get(quality_text, 26)
    suffix = f"preset{val}" if val < 13 else f"qvbr{val}"
    src_dir = src.parent
    out_dir = src_dir
    
    if file_count_in_dir > 1:
        out_dir = src_dir / output_dir_name
        out_dir.mkdir(exist_ok=True)
    
    return str(out_dir / f"{src.stem}_comp_{suffix}.mkv"), str(out_dir)
