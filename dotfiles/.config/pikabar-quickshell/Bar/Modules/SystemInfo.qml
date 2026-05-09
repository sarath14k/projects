import QtQuick
import Quickshell
import Quickshell.Io
import qs.Settings
import qs.Services
import qs.Components
Row {
    id: layout
    spacing: 12
    visible: Settings.settings.showSystemInfoInBar

    property bool showGpuStats: false

    Binding {
        target: Sysinfo
        property: "weatherCity"
        value: Settings.settings.weatherCity
    }

    Timer {
        interval: 3000
        running: true
        repeat: true
        onTriggered: showGpuStats = !showGpuStats
    }

    Item {
        id: cpuUsageItem
        implicitWidth: cpuUsageLayout.implicitWidth
        implicitHeight: cpuUsageLayout.implicitHeight
        width: implicitWidth
        height: implicitHeight

        Process {
            id: cpuProcess
            command: ["bash", "-c", "ps axo pid,pcpu,comm --sort=-pcpu | head -n 11 | awk 'BEGIN {printf \"%-20s %-12s %-8s\\n--------------------------------------------\\n\", \"PROGRAM\", \"CPU%\", \"PID\"} NR>1 {printf \"%-20s %-12s %-8s\\n\", $3, $2\"%\", $1}'"]
            stdout: StdioCollector {}
            onExited: {
                cpuTooltip.text = String(stdout.text).trim() || "No data";
                if (cpuMouseArea.containsMouse) {
                    cpuTooltip.tooltipVisible = true;
                }
            }
        }

        StyledTooltip {
            id: cpuTooltip
            targetItem: cpuUsageItem
            positionAbove: false
            textAlignment: Text.AlignLeft
            fontOverride: "monospace"
            text: "Loading..."
        }

        Row {
            id: cpuUsageLayout
            spacing: 6

            Text {
                id: cpuUsageIcon
                font.family: "Material Symbols Outlined"
                font.pixelSize: Theme.fontSizeBody * Theme.scale(Screen)
                text: "memory" // CPU Chip icon
                verticalAlignment: Text.AlignVCenter
                anchors.verticalCenter: parent.verticalCenter
                color: "#00D1FF" // CPU Electric Blue
            }

            Text {
                id: cpuUsageText
                font.family: Theme.fontFamily
                font.pixelSize: Theme.fontSizeSmall * Theme.scale(Screen)
                color: Theme.textPrimary
                text: Sysinfo.cpuUsageStr
                anchors.verticalCenter: parent.verticalCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        MouseArea {
            id: cpuMouseArea
            anchors.fill: parent
            hoverEnabled: true
            onEntered: {
                cpuProcess.running = true;
            }
            onExited: {
                cpuTooltip.tooltipVisible = false;
            }
        }
    }

    // Toggle: CPU Temp <-> GPU Temp
    Row {
        id: tempLayout
        spacing: 6
        Text {
            font.family: "Material Symbols Outlined"
            font.pixelSize: Theme.fontSizeBody * Theme.scale(Screen)
            text: showGpuStats ? "videogame_asset" : "device_thermostat" // GPU controller vs CPU Temp
            verticalAlignment: Text.AlignVCenter
            anchors.verticalCenter: parent.verticalCenter
            color: {
                const temp = showGpuStats ? Sysinfo.gpuTemp : Sysinfo.cpuTemp;
                if (temp >= 80) return "#FF3B30"; // Red
                if (temp >= 65) return "#FFCC00"; // Yellow
                return "#00D1FF"; // Blue
            }
        }

        Text {
            font.family: Theme.fontFamily
            font.pixelSize: Theme.fontSizeSmall * Theme.scale(Screen)
            color: Theme.textPrimary
            text: showGpuStats ? Sysinfo.gpuTempStr : Sysinfo.cpuTempStr
            anchors.verticalCenter: parent.verticalCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    // Toggle: RAM Usage <-> GPU Memory Usage
    Item {
        id: memItem
        implicitWidth: memoryUsageLayout.implicitWidth
        implicitHeight: memoryUsageLayout.implicitHeight
        width: implicitWidth
        height: implicitHeight

        Process {
            id: memProcess
            command: ["bash", "-c", "ps axo pid,rss,comm --sort=-rss | head -n 11 | awk 'BEGIN {printf \"%-20s %-12s %-8s\\n--------------------------------------------\\n\", \"PROGRAM\", \"RAM\", \"PID\"} NR>1 {printf \"%-20s %-12s %-8s\\n\", $3, sprintf(\"%.1f MB\", $2/1024), $1}'"]
            stdout: StdioCollector {}
            onExited: {
                memTooltip.text = String(stdout.text).trim() || "No data";
                if (memMouseArea.containsMouse) {
                    memTooltip.tooltipVisible = true;
                }
            }
        }

        StyledTooltip {
            id: memTooltip
            targetItem: memItem
            positionAbove: false
            textAlignment: Text.AlignLeft
            fontOverride: "monospace"
            text: "Loading..."
        }

        Row {
            id: memoryUsageLayout
            spacing: 6

            Text {
                font.family: "Material Symbols Outlined"
                font.pixelSize: Theme.fontSizeBody * Theme.scale(Screen)
                text: showGpuStats ? "developer_board" : "database" // VRAM board vs RAM database
                color: showGpuStats ? "#BF5AF2" : "#FFD700" // Purple for VRAM, Yellow for RAM
                verticalAlignment: Text.AlignVCenter
                anchors.verticalCenter: parent.verticalCenter
            }

            Text {
                font.family: Theme.fontFamily
                font.pixelSize: Theme.fontSizeSmall * Theme.scale(Screen)
                color: Theme.textPrimary
                text: showGpuStats ? Sysinfo.gpuMemUsageStr : Sysinfo.memoryUsageStr
                anchors.verticalCenter: parent.verticalCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        MouseArea {
            id: memMouseArea
            anchors.fill: parent
            hoverEnabled: true
            onEntered: {
                memProcess.running = true;
            }
            onExited: {
                memTooltip.tooltipVisible = false;
            }
        }
    }

    // Room Temp
    Item {
        id: roomTempItem
        implicitWidth: roomTempLayout.implicitWidth
        implicitHeight: roomTempLayout.implicitHeight
        width: implicitWidth
        height: implicitHeight

        Process {
            id: tempProcess
            command: ["python3", "/home/sarath/.config/pikabar-quickshell/scripts/sys_temps.py"]
            stdout: StdioCollector {}
            onExited: {
                tempTooltip.text = String(stdout.text).trim() || "No data";
                if (roomTempMouseArea.containsMouse) {
                    tempTooltip.tooltipVisible = true;
                }
            }
        }

        Process {
            id: copyProcess
            command: ["bash", "-c", "python3 /home/sarath/.config/pikabar-quickshell/scripts/sys_temps.py | wl-copy && notify-send 'System Temperatures' 'Copied to clipboard!' -t 2000"]
        }

        MouseArea {
            id: roomTempMouseArea
            anchors.fill: parent
            hoverEnabled: true
            acceptedButtons: Qt.RightButton
            onEntered: {
                tempProcess.running = true;
            }
            onExited: {
                tempTooltip.tooltipVisible = false;
            }
            onClicked: {
                copyProcess.running = true;
            }
        }
        
        StyledTooltip {
            id: tempTooltip
            targetItem: roomTempItem
            positionAbove: false
            textAlignment: Text.AlignLeft
            fontOverride: "monospace"
            text: "Loading..."
        }

        Row {
            id: roomTempLayout
            spacing: 12 // Space between local and online weather
            
            // Local Ambient
            Row {
                spacing: 6
                Text {
                    font.family: "Material Symbols Outlined"
                    font.pixelSize: Theme.fontSizeBody * Theme.scale(Screen)
                    text: "developer_board"
                    color: "#00FF7F" // Spring Green
                    verticalAlignment: Text.AlignVCenter
                    anchors.verticalCenter: parent.verticalCenter
                }

                Text {
                    font.family: Theme.fontFamily
                    font.pixelSize: Theme.fontSizeSmall * Theme.scale(Screen)
                    color: Theme.textPrimary
                    text: Sysinfo.roomTempStr
                    anchors.verticalCenter: parent.verticalCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }

            // Online Weather
            Row {
                spacing: 6
                visible: Settings.settings.weatherCity !== ""
                Text {
                    font.family: "Material Symbols Outlined"
                    font.pixelSize: Theme.fontSizeBody * Theme.scale(Screen)
                    text: "home"
                    color: "#00D1FF" // Sky Blue
                    verticalAlignment: Text.AlignVCenter
                    anchors.verticalCenter: parent.verticalCenter
                }

                Text {
                    font.family: Theme.fontFamily
                    font.pixelSize: Theme.fontSizeSmall * Theme.scale(Screen)
                    color: Theme.textPrimary
                    text: Sysinfo.weatherTempStr
                    anchors.verticalCenter: parent.verticalCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
        }

    }

    // Storage Space
    Item {
        id: storageItem
        implicitWidth: storageLayout.implicitWidth
        implicitHeight: storageLayout.implicitHeight
        width: implicitWidth
        height: implicitHeight

        Process {
            id: storageProcess
            command: ["bash", "-c", "df -h | grep '^/dev/' | awk 'BEGIN {printf \"%-12s %-6s %-6s %-6s %-5s\\n---------------------------------------\\n\", \"MOUNT\", \"SIZE\", \"USED\", \"AVAIL\", \"USE%\"} {printf \"%-12s %-6s %-6s %-6s %-5s\\n\", $6, $2, $3, $4, $5}'"]
            stdout: StdioCollector {}
            onExited: {
                storageTooltip.text = String(stdout.text).trim() || "No data";
                if (storageMouseArea.containsMouse) {
                    storageTooltip.tooltipVisible = true;
                }
            }
        }

        StyledTooltip {
            id: storageTooltip
            targetItem: storageItem
            positionAbove: false
            textAlignment: Text.AlignLeft
            fontOverride: "monospace"
            text: "Loading..."
        }

        Row {
            id: storageLayout
            spacing: 6
            Text {
                font.family: "Material Symbols Outlined"
                font.pixelSize: Theme.fontSizeBody * Theme.scale(Screen)
                text: "hard_drive"
                color: "#FF9F0A" // Orange
                verticalAlignment: Text.AlignVCenter
                anchors.verticalCenter: parent.verticalCenter
            }
            Text {
                font.family: Theme.fontFamily
                font.pixelSize: Theme.fontSizeSmall * Theme.scale(Screen)
                color: Theme.textPrimary
                text: "Disk"
                anchors.verticalCenter: parent.verticalCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        MouseArea {
            id: storageMouseArea
            anchors.fill: parent
            hoverEnabled: true
            onEntered: {
                storageProcess.running = true;
            }
            onExited: {
                storageTooltip.tooltipVisible = false;
            }
        }
    }
}
