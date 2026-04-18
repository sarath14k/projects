#!/bin/bash

echo "🗑️ Starting MeetShare Pro Uninstallation..."

# 1. Kill the bridge process
echo "🛑 Stopping the background bridge..."
pkill -f mpv_bridge.py

# 2. Remove Universal Startup (.desktop file)
echo "📂 Removing autostart entries..."
rm -f "$HOME/.config/autostart/meetshare.desktop"

# 3. Remove Hyprland Startup Entry
HYPR_CONF="$HOME/.config/hypr/hyprland.conf"
if [ -f "$HYPR_CONF" ]; then
    echo "🖥️ Cleaning Hyprland config..."
    # Remove lines containing mpv_bridge.py
    sed -i '/mpv_bridge.py/d' "$HYPR_CONF"
fi

echo "-------------------------------------------------------"
echo "✅ UNINSTALLATION COMPLETE!"
echo "-------------------------------------------------------"
echo "Note: System dependencies (mpv, pipewire, etc.) were kept"
echo "as they may be used by other applications."
echo ""
echo "To completely remove the files, you can delete this folder:"
echo "rm -rf $(pwd)"
echo "-------------------------------------------------------"
