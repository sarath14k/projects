import QtQuick 
import QtQuick.Layouts
import QtQuick.Controls
import Quickshell.Io
import qs.Components
import qs.Services
import qs.Settings

Rectangle {
    id: systemMonitor
    color: "transparent"

    // Track visibility state for panel integration
    property bool isVisible: false
    property bool showDetails: false

    Rectangle {
        id: card
        anchors.fill: parent
        color: Theme.surface
        radius: 18 * Theme.scale(Screen)
        border.color: showDetails ? Theme.accentPrimary : "transparent"
        border.width: 2 * Theme.scale(Screen)

        MouseArea {
            id: cardMouse
            anchors.fill: parent
            onClicked: showDetails = !showDetails
            hoverEnabled: true

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 8 * Theme.scale(screen)
                spacing: 12 * Theme.scale(screen)
                Layout.alignment: Qt.AlignVCenter

        
                // CPU usage indicator with circular progress bar
                Item {
                    width: 50 * Theme.scale(screen)
                    height: 50 * Theme.scale(screen)
                    CircularProgressBar {
                        id: cpuBar
                        progress: Sysinfo.cpuUsage / 100
                        size: 50 * Theme.scale(screen)
                        strokeWidth: 4 * Theme.scale(screen)
                        hasNotch: true
                        notchIcon: "speed"
                        notchIconSize: 14 * Theme.scale(screen)
                        Layout.alignment: Qt.AlignHCenter
                    }
                    MouseArea {
                        id: cpuBarMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: cpuTooltip.tooltipVisible = true
                        onExited: cpuTooltip.tooltipVisible = false
                    }
                    StyledTooltip {
                        id: cpuTooltip
                        text: 'CPU Usage: ' + Sysinfo.cpuUsage + '%'
                        tooltipVisible: false
                        targetItem: cpuBar
                        delay: 200
                    }
                }

        
                // CPU temperature indicator with circular progress bar
                Item {
                    width: 50 * Theme.scale(screen); height: 50 * Theme.scale(screen)
                    CircularProgressBar {
                        id: tempBar
                        progress: Sysinfo.cpuTemp / 100
                        size: 50 * Theme.scale(screen)
                        strokeWidth: 4 * Theme.scale(screen)
                        hasNotch: true
                        units: "°C"
                        notchIcon: "thermometer"
                        notchIconSize: 14 * Theme.scale(screen)
                        Layout.alignment: Qt.AlignHCenter
                    }
                    MouseArea {
                        id: tempBarMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: tempTooltip.tooltipVisible = true
                        onExited: tempTooltip.tooltipVisible = false
                    }
                    StyledTooltip {
                        id: tempTooltip
                        text: 'CPU Temp: ' + Sysinfo.cpuTemp + '°C'
                        tooltipVisible: false
                        targetItem: tempBar
                        delay: 200
                    }
                }

        
                // Memory usage indicator with circular progress bar
                Item {
                    width: 50 * Theme.scale(screen); height: 50 * Theme.scale(screen)
                    CircularProgressBar {
                        id: memBar
                        progress: Sysinfo.memoryUsagePer / 100
                        size: 50 * Theme.scale(screen)
                        strokeWidth: 4 * Theme.scale(screen)
                        hasNotch: true
                        notchIcon: "memory"
                        notchIconSize: 14 * Theme.scale(screen)
                        Layout.alignment: Qt.AlignHCenter
                    }
                    MouseArea {
                        id: memBarMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: memTooltip.tooltipVisible = true
                        onExited: memTooltip.tooltipVisible = false
                    }
                    StyledTooltip {
                        id: memTooltip
                        text: 'Memory Usage: ' + Sysinfo.memoryUsagePer + '% (' + Sysinfo.memoryUsageStr + ' used)'
                        tooltipVisible: false
                        targetItem: memBar
                        delay: 200
                    }
                }

        
                // Disk usage indicator with circular progress bar
                Item {
                    width: 50 * Theme.scale(screen); height: 50 * Theme.scale(screen)
                    CircularProgressBar {
                        id: diskBar
                        progress: Sysinfo.diskUsage / 100
                        size: 50 * Theme.scale(screen)
                        strokeWidth: 4 * Theme.scale(screen)
                        hasNotch: true
                        notchIcon: "storage"
                        notchIconSize: 14 * Theme.scale(screen)
                        Layout.alignment: Qt.AlignHCenter
                    }
                    MouseArea {
                        id: diskBarMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: diskTooltip.tooltipVisible = true
                        onExited: diskTooltip.tooltipVisible = false
                    }
                    StyledTooltip {
                        id: diskTooltip
                        text: 'Disk Usage: ' + Sysinfo.diskUsage + '%'
                        tooltipVisible: false
                        targetItem: diskBar
                        delay: 200
                    }
                }
            }

            Text {
                id: detailsHint
                anchors.bottom: parent.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottomMargin: 4 * Theme.scale(screen)
                text: showDetails ? "expand_less" : "expand_more"
                font.family: "Material Symbols Outlined"
                font.pixelSize: 14 * Theme.scale(screen)
                color: Theme.accentPrimary
                opacity: (cardMouse.containsMouse || showDetails) ? 1 : 0
                Behavior on opacity { NumberAnimation { duration: 200 } }
            }
        }
    }
}