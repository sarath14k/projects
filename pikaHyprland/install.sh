#!/bin/bash

# MeetShare Pro - One-Click Installer for PikaOS/Hyprland
echo "🚀 Starting MeetShare Pro Installation..."

# 1. Install System Dependencies
echo "📦 Installing dependencies (mpv, zenity, pipewire-tools)..."
sudo apt update && sudo apt install -y mpv zenity pipewire-bin python3

# 2. Get Current Directory
INSTALL_DIR=$(pwd)
BRIDGE_PATH="$INSTALL_DIR/mpv_bridge.py"

# 3. Add to Hyprland Startup
HYPR_CONF="$HOME/.config/hypr/hyprland.conf"
if [ -f "$HYPR_CONF" ]; then
    if ! grep -q "mpv_bridge.py" "$HYPR_CONF"; then
        echo "🖥️ Adding MeetShare to Hyprland startup..."
        echo "exec-once = python3 \"$BRIDGE_PATH\"" >> "$HYPR_CONF"
    else
        echo "✅ MeetShare already in Hyprland startup."
    fi
else
    echo "⚠️ Hyprland config not found at $HYPR_CONF. Please add 'exec-once = python3 \"$BRIDGE_PATH\"' manually."
fi

# 4. Start the Bridge Now
echo "🌐 Starting the bridge in the background..."
pkill -f mpv_bridge.py
python3 "$BRIDGE_PATH" > /dev/null 2>&1 & disown

# 5. Final Instructions
echo ""
echo "-------------------------------------------------------"
echo "🎉 INSTALLATION COMPLETE!"
echo "-------------------------------------------------------"
echo "1. Open Chrome and go to: chrome://extensions"
echo "2. Enable 'Developer Mode' (top right)."
echo "3. Click 'Load unpacked' and select this folder:"
echo "   $INSTALL_DIR/meet_extension"
echo ""
echo "4. Your Dashboard is live at: http://127.0.0.1:9999/"
echo "-------------------------------------------------------"
