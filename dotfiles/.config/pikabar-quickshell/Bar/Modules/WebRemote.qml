import QtQuick
import QtQuick.Controls
import Quickshell
import Quickshell.Io

Item {
    id: root
    property var screen
    width: 32
    height: 32

    property bool isActive: false
    property string statusText: "..."

    Process {
        id: statusProcess
        command: ["bash", "-c", "systemctl --user is-active webremote || echo inactive"]
        stdout: StdioCollector {}
        onExited: {
            let output = String(stdout.text).trim();
            isActive = (output === "active");
            statusText = output;
        }
    }

    Process {
        id: toggleProcess
        command: ["bash", "-c", "/home/sarath/projects/toggle_remote.sh"]
        onExited: statusProcess.running = true
    }

    Timer {
        interval: 3000
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: if (!toggleProcess.running) statusProcess.running = true
    }

    Text {
        anchors.centerIn: parent
        text: isActive ? "settings_remote" : "mobile_off"
        font.family: "Material Symbols Outlined"
        font.pixelSize: 20
        color: isActive ? "#90EE90" : "#FF6B6B"
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: {
            toggleProcess.running = true;
            statusText = "toggling...";
        }

        ToolTip {
            visible: parent.containsMouse
            text: "Web Remote: " + root.statusText + "\nIP: 192.168.1.12:5000"
            delay: 500
        }
    }
}
