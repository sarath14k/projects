import QtQuick
import Quickshell
import Quickshell.Io
import qs.Settings
import qs.Components

Item {
    id: powerModeModule
    implicitWidth: powerModeLayout.implicitWidth
    implicitHeight: powerModeLayout.implicitHeight
    width: implicitWidth
    height: 36 * Theme.scale(Screen) // Match bar height

    property string currentMode: "Checking..."
    property string governor: ""

    Process {
        id: powerProcess
        command: ["bash", "-c", "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"]
        stdout: StdioCollector {}
        onExited: {
            governor = String(stdout.text).trim();
            if (governor === "performance") {
                currentMode = "Performance";
            } else {
                currentMode = "Economy";
            }
        }
    }

    Process {
        id: switchProcess
    }

    Timer {
        interval: 3000
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: if (!switchProcess.running) powerProcess.running = true
    }

    Row {
        id: powerModeLayout
        spacing: 6
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        Text {
            font.family: "Material Symbols Outlined"
            font.pixelSize: Theme.fontSizeBody * Theme.scale(Screen)
            text: currentMode === "Performance" ? "bolt" : "eco"
            verticalAlignment: Text.AlignVCenter
            anchors.verticalCenter: parent.verticalCenter
            color: currentMode === "Performance" ? "#FFD700" : "#90EE90"
        }
    }

    MouseArea {
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        onClicked: (mouse) => {
            if (mouse.button === Qt.LeftButton) {
                if (currentMode === "Performance") {
                    switchProcess.command = ["bash", "-c", "echo 'sa' | sudo -S auto-cpufreq --force powersave"];
                } else {
                    switchProcess.command = ["bash", "-c", "echo 'sa' | sudo -S auto-cpufreq --force performance"];
                }
            } else if (mouse.button === Qt.RightButton) {
                switchProcess.command = ["bash", "-c", "echo 'sa' | sudo -S auto-cpufreq --force reset"];
            }
            switchProcess.running = true;
            currentMode = "Switching...";
        }
    }
    
    StyledTooltip {
        text: "Current Mode: " + currentMode + "\nLeft Click: Toggle Performance/Economy\nRight Click: Reset to Automatic"
        targetItem: powerModeModule
    }
}
