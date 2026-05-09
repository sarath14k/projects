import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Io
import qs.Settings
import qs.Components

Item {
    id: root
    
    property string ethStatus: "disconnected"

    implicitWidth: ethIcon.implicitWidth + 8 * Theme.scale(Screen)
    implicitHeight: 22 * Theme.scale(Screen)
    width: implicitWidth
    height: implicitHeight

    // Check networking status
    Timer {
        id: statusTimer
        interval: 30000 // 30s
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: statusProcess.running = true
    }

    Process {
        id: statusProcess
        // Check specific ethernet interface state via nmcli
        command: ["nmcli", "-t", "-f", "GENERAL.STATE", "device", "show", "enp13s0"]
        stdout: StdioCollector {
            onStreamFinished: {
                root.ethStatus = text.includes("(connected)") ? "connected" : "disconnected";
            }
        }
    }

    Process {
        id: ethToggleProcess
        property string action: "connect"
        command: ["nmcli", "device", action, "enp13s0"]
        onExited: statusProcess.running = true
    }

    Item {
        anchors.centerIn: parent
        width: ethIcon.implicitWidth
        height: ethIcon.implicitHeight

        Text {
            id: ethIcon
            anchors.centerIn: parent
            text: "lan"
            font.family: mouseArea.containsMouse ? "Material Symbols Rounded" : "Material Symbols Outlined"
            font.pixelSize: 18 * Theme.scale(Screen)
            color: root.ethStatus === "connected" ? "#4CAF50" : "#F44336"
            
            Behavior on color {
                ColorAnimation { duration: 300 }
            }
        }

        Text {
            id: crossIcon
            anchors.centerIn: parent
            text: "close"
            font.family: "Material Symbols Outlined"
            font.pixelSize: 14 * Theme.scale(Screen)
            color: "#F44336"
            visible: root.ethStatus !== "connected"
            opacity: 0.8
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: {
            if (!ethToggleProcess.running) {
                ethToggleProcess.action = root.ethStatus === "connected" ? "disconnect" : "connect";
                ethToggleProcess.running = true;
            }
        }
    }

    StyledTooltip {
        id: ethTooltip
        text: "Networking: " + root.ethStatus
        positionAbove: false
        tooltipVisible: mouseArea.containsMouse
        targetItem: root
    }
}
