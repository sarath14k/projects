# Video Converter (GTK3)

A lightweight, GPU-accelerated batch video compressor for Linux. Built with Python and GTK3, it provides a simple drag-and-drop interface for FFmpeg, optimizing videos for size while maintaining quality using modern codecs (HEVC/AV1).

![App Icon](video_converter.png)

## Features

* **GPU Acceleration**: Supports VAAPI for Intel and AMD, and NVENC/NVDEC for NVIDIA (via FFmpeg configuration).
* **Batch Processing**: Queue multiple files and convert them sequentially.
* **Drag & Drop**: Easily add videos by dragging them into the window.
* **Smart Compression**:
    * **HEVC (H.265)**: 10-bit and 8-bit support.
    * **AV1**: Future-proof compression (SVT-AV1 or VAAPI).
* **Quality Presets**: Simple slider-based quality targets (e.g., "Best", "High", "Lite").
* **Auto-Cleanup**: Option to automatically move source files to trash or delete them after successful conversion.
* **System Integration**: Prevents system sleep during encoding and integrates with the desktop taskbar.

## Supported Distributions

The installer script automatically detects your package manager and installs necessary dependencies for:
* **Arch Linux / CachyOS / Manjaro** (`pacman`)
* **Ubuntu / Debian / Pop!_OS** (`apt`)
* **Fedora / RHEL** (`dnf`)
* **openSUSE** (`zypper`)
* **Void Linux** (`xbps`)

## Prerequisites

* Python 3.8+
* FFmpeg & FFprobe
* GTK3 & PyGObject
* Trash-CLI (for moving source files to trash)

*Note: The `install.sh` script attempts to install these automatically.*

## Installation

### 1. Quick Install (Recommended)

1.  Download or extract the source code.
2.  Open a terminal in the folder.
3.  Run the installer:

    ```bash
    chmod +x install.sh uninstall.sh
    ./install.sh
    ```

This will:
* Install system dependencies (`ffmpeg`, `python3-gi`, etc.).
* Create a desktop shortcut in `~/.local/share/applications/`.
* Set up the application icon.

You can now launch **"Video Converter"** from your system's application menu.

### 2. Manual Run (Development)

If you prefer not to install the desktop shortcut, you can run the application directly from the source:

```bash
# Install dependencies manually (example for Arch)
sudo pacman -S python-gobject gtk3 ffmpeg trash-cli

# Run the app
python3 src/main.py
