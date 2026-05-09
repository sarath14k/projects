import QtQuick 
import Quickshell
import Quickshell.Io
import qs.Settings
import qs.Components

Item {
    id: root
    width: 26 * Theme.scale(Screen); height: 26 * Theme.scale(Screen)
    
    property var shell: null

    Process {
        id: updateProcess
        command: ["kitty", "sh", "-c", "echo 'Starting System Update...'; pikman update && pikman upgrade; echo; echo 'Process finished. Press Enter to close.'; read"]
    }

    Process {
        id: cosmicProcess
        command: ["cosmic-store"]
    }

    Item {
        id: updateButton
        anchors.fill: parent
        
        Text {
            id: internalIcon
            anchors.centerIn: parent
            text: "sync" // Material Symbols Rounded refresh/sync icon
            font.family: mouseArea.containsMouse ? "Material Symbols Rounded" : "Material Symbols Outlined"
            font.pixelSize: 18 * Theme.scale(Screen)
            color: mouseArea.containsMouse ? Theme.accentPrimary : Theme.textDisabled
            
            Behavior on color { ColorAnimation { duration: 200 } }
        }

        MouseArea {
            id: mouseArea
            anchors.fill: parent
            hoverEnabled: true
            acceptedButtons: Qt.LeftButton | Qt.RightButton
            cursorShape: Qt.PointingHandCursor
            onClicked: (mouse) => {
                if (mouse.button === Qt.LeftButton) {
                    cosmicProcess.running = true;
                } else if (mouse.button === Qt.RightButton) {
                    updateProcess.running = true;
                }
            }
            onEntered: tooltip.tooltipVisible = true
            onExited: tooltip.tooltipVisible = false
        }
    }

    StyledTooltip {
        id: tooltip
        text: "L: Cosmic Store | R: Pikman Update"
        positionAbove: false
        tooltipVisible: false
        targetItem: updateButton
        delay: 200
    }
}
