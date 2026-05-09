import Quickshell
import Quickshell.Hyprland
import QtQuick

ShellRoot {
    Component.onCompleted: {
        try {
            console.log("Active Window ID:", Hyprland.activeWindow.address);
        } catch(e) {
            console.log("Hyprland.activeWindow not available or no active window");
        }
        Qt.quit();
    }
}
