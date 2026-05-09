import QtQuick
import Quickshell
import Quickshell.Io
import qs.Settings
import qs.Services
import qs.Components

Item {
    id: networkItem
    implicitWidth: layout.implicitWidth
    implicitHeight: layout.implicitHeight
    width: implicitWidth
    height: implicitHeight
    anchors.verticalCenter: parent.verticalCenter

    Process {
        id: netProcess
        command: ["bash", "-c", "echo \"Local IP: $(ip route get 1.1.1.1 | awk '{print $7; exit}')\"; echo \"Ping: $(ping -c 1 8.8.8.8 | awk -F'/' 'END{print $5}') ms\""]
        stdout: StdioCollector {}
        onExited: {
            netTooltip.text = String(stdout.text).trim() || "No data";
            if (netMouseArea.containsMouse) {
                netTooltip.tooltipVisible = true;
            }
        }
    }

    Process {
        id: copyProcess
        command: ["bash", "-c", "echo \"Local IP: $(ip route get 1.1.1.1 | awk '{print $7; exit}')\nPing: $(ping -c 1 8.8.8.8 | awk -F'/' 'END{print $5}') ms\" | wl-copy && notify-send 'Network Info' 'Copied to clipboard!' -t 2000"]
    }

    StyledTooltip {
        id: netTooltip
        targetItem: networkItem
        positionAbove: false
        textAlignment: Text.AlignLeft
        fontOverride: "monospace"
        text: "Loading..."
    }

    Row {
        id: layout
        spacing: 12
        anchors.centerIn: parent

        Row {
            spacing: 4
            Text {
                font.family: "Material Symbols Outlined"
                font.pixelSize: Theme.fontSizeBody * Theme.scale(Screen)
                text: "download"
                color: Theme.accentPrimary
                verticalAlignment: Text.AlignVCenter
                anchors.verticalCenter: parent.verticalCenter
            }
            Text {
                font.family: Theme.fontFamily
                font.pixelSize: Theme.fontSizeSmall * Theme.scale(Screen)
                color: Theme.textPrimary
                text: NetworkSpeed.downloadSpeedStr
                verticalAlignment: Text.AlignVCenter
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        Row {
            spacing: 4
            Text {
                font.family: "Material Symbols Outlined"
                font.pixelSize: Theme.fontSizeBody * Theme.scale(Screen)
                text: "upload"
                color: Theme.accentPrimary
                verticalAlignment: Text.AlignVCenter
                anchors.verticalCenter: parent.verticalCenter
            }
            Text {
                font.family: Theme.fontFamily
                font.pixelSize: Theme.fontSizeSmall * Theme.scale(Screen)
                color: Theme.textPrimary
                text: NetworkSpeed.uploadSpeedStr
                verticalAlignment: Text.AlignVCenter
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }

    MouseArea {
        id: netMouseArea
        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.RightButton
        onEntered: {
            netProcess.running = true;
        }
        onExited: {
            netTooltip.tooltipVisible = false;
        }
        onClicked: {
            copyProcess.running = true;
        }
    }
}
