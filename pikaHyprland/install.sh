#!/bin/bash

echo "🚀 Starting MeetShare Pro Universal Installer..."

# 1. Detect Package Manager and Install Dependencies
if command -v apt &> /dev/null; then
    sudo apt update && sudo apt install -y mpv zenity pipewire-bin python3
elif command -v dnf &> /dev/null; then
    sudo dnf install -y mpv zenity pipewire-utils python3
elif command -v pacman &> /dev/null; then
    sudo pacman -S --noconfirm mpv zenity pipewire python3
else
    echo "❌ Unknown package manager. Please install mpv, zenity, pipewire, and python3 manually."
fi

# 2. Get Paths
INSTALL_DIR=$(pwd)
BRIDGE_PATH="$INSTALL_DIR/mpv_bridge.py"

# 3. Universal Linux Autostart (XDG Desktop Entry)
AUTOSTART_DIR="$HOME/.config/autostart"
mkdir -p "$AUTOSTART_DIR"
cat <<EOF > "$AUTOSTART_DIR/meetshare.desktop"
[Desktop Entry]
Type=Application
Exec=python3 "$BRIDGE_PATH"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=MeetShare Bridge
Comment=Media Sharing Bridge for Google Meet
EOF

# 4. Hyprland Specific (Keep as fallback)
HYPR_CONF="$HOME/.config/hypr/hyprland.conf"
if [ -f "$HYPR_CONF" ]; then
    if ! grep -q "mpv_bridge.py" "$HYPR_CONF"; then
        echo "exec-once = python3 \"$BRIDGE_PATH\"" >> "$HYPR_CONF"
    fi
fi

# 5. Start Now
pkill -f mpv_bridge.py
python3 "$BRIDGE_PATH" > /dev/null 2>&1 & disown

echo "🎉 Universal Installation Complete!"
echo "Your dashboard is live at: http://127.0.0.1:9999/"
