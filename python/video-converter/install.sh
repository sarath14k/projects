#!/bin/bash

# Get the absolute path of the directory containing this script
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ICON_PATH="$INSTALL_DIR/video_converter.png"
EXEC_PATH="$INSTALL_DIR/src/main.py"
DESKTOP_FILE="$HOME/.local/share/applications/video-converter.desktop"

echo "Checking for dependencies..."

if command -v apt-get &> /dev/null; then
    echo "Ubuntu/Debian detected. Installing dependencies..."
    sudo apt-get update
    sudo apt-get install -y python3-gi gir1.2-gtk-3.0 ffmpeg trash-cli python3-gi-cairo

elif command -v pacman &> /dev/null; then
    echo "Arch Linux detected. Installing dependencies..."
    sudo pacman -S --needed --noconfirm python-gobject gtk3 ffmpeg trash-cli

elif command -v dnf &> /dev/null; then
    echo "Fedora/RHEL detected. Installing dependencies..."
    sudo dnf install -y python3-gobject gtk3 ffmpeg trash-cli

elif command -v zypper &> /dev/null; then
    echo "openSUSE detected. Installing dependencies..."
    sudo zypper install -n python3-gobject gtk3 ffmpeg trash-cli

elif command -v xbps-install &> /dev/null; then
    echo "Void Linux detected. Installing dependencies..."
    sudo xbps-install -Sy python3-gobject gtk3 ffmpeg trash-cli
else
    echo "⚠️  Unknown package manager. Please ensure 'python3-gobject', 'gtk3', 'ffmpeg', and 'trash-cli' are installed manually."
fi

# Check if icon exists, fallback to generic
if [ ! -f "$ICON_PATH" ]; then
    ICON_VAL="video-x-generic"
else
    ICON_VAL="$ICON_PATH"
fi

# Ensure executable permissions
chmod +x "$EXEC_PATH"

# Create Desktop Entry
mkdir -p "$HOME/.local/share/applications"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Name=Video Converter
Exec=$EXEC_PATH
Icon=$ICON_VAL
Type=Application
Terminal=false
Categories=AudioVideo;Video;Utility;
Comment=GPU Accelerated Video Compressor
StartupWMClass=video-converter
EOF

if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$HOME/.local/share/applications" 2>/dev/null
fi

echo "------------------------------------------"
echo "✅ Installation Successful!"
echo "You can now launch 'Video Converter' from your app menu."
