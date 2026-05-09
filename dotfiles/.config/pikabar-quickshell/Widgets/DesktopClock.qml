import QtQuick
import QtQuick.Effects
import qs.Bar.Modules
import qs.Settings
import qs.Components
import qs.Services

Item {
    id: root
    property var screen: null
    
    // Optimized: Use centralized Theme scaling
    readonly property real screenScale: Theme.scale(screen)

    width: clockColumn.width
    height: clockColumn.height

    // Deep Glass Background
    Rectangle {
        id: bg
        anchors.centerIn: clockColumn
        width: clockColumn.width + 80 * screenScale
        height: clockColumn.height + 60 * screenScale
        radius: 30 * screenScale
        color: "#14000000"
        border.color: "#1AFFFFFF"
        border.width: 1
        
        layer.enabled: true
        layer.effect: MultiEffect {
            blurEnabled: true
            blur: 1.0 
            shadowEnabled: true
            shadowColor: "#B3000000"
            shadowBlur: 0.8
        }
    }

    Column {
        id: clockColumn
        spacing: 15 * root.screenScale

        // Performance Row
        Row {
            anchors.right: parent.right
            spacing: 20 * root.screenScale
            opacity: (Sysinfo.cpuUsage > 50 || Sysinfo.memoryUsagePer > 50) ? 0.5 : 0.0
            Behavior on opacity { NumberAnimation { duration: 500 } }
            
            Column {
                spacing: 4
                Text { 
                    text: "CPU " + Sysinfo.cpuUsageStr
                    font.family: Theme.fontFamily
                    font.pixelSize: 11 * root.screenScale
                    font.weight: Font.Bold
                    color: "white"
                    anchors.right: parent.right
                    opacity: 0.6
                }
                Rectangle {
                    width: 70 * root.screenScale; height: 2; radius: 1; color: "#1AFFFFFF"
                    Rectangle {
                        width: parent.width * (Sysinfo.cpuUsage / 100); height: parent.height; radius: parent.radius
                        color: Theme.accentPrimary
                    }
                }
            }
            Column {
                spacing: 4
                Text { 
                    text: "RAM " + Sysinfo.memoryUsagePerStr
                    font.family: Theme.fontFamily
                    font.pixelSize: 11 * root.screenScale
                    font.weight: Font.Bold
                    color: "white"
                    anchors.right: parent.right
                    opacity: 0.6
                }
                Rectangle {
                    width: 70 * root.screenScale; height: 2; radius: 1; color: "#1AFFFFFF"
                    Rectangle {
                        width: parent.width * (Sysinfo.memoryUsagePer / 100); height: parent.height; radius: parent.radius
                        color: Theme.accentPrimary
                    }
                }
            }
        }

        // Clock Section
        Column {
            anchors.right: parent.right
            spacing: -18 * root.screenScale
            
            Text {
                id: timeText
                text: Time.time
                font.family: Theme.fontFamily
                font.weight: Font.Black
                font.pixelSize: 120 * root.screenScale
                color: "white"
                opacity: 0.5 // Set to 0.5 as requested
                layer.enabled: true
                layer.effect: MultiEffect {
                    blurEnabled: true; blur: 0.03
                    shadowEnabled: true; shadowColor: "#80000000"; shadowBlur: 0.6
                }
            }

            Row {
                anchors.right: parent.right
                anchors.rightMargin: 12 * root.screenScale
                
                Text {
                    text: Time.dateString.toUpperCase()
                    font.family: Theme.fontFamily
                    font.weight: Font.DemiBold
                    font.pixelSize: 26 * root.screenScale
                    color: "white"
                    opacity: 0.6 // Kept at 0.6 as requested
                    font.letterSpacing: 2.5
                    layer.enabled: true
                    layer.effect: MultiEffect {
                        shadowEnabled: true; shadowColor: Theme.accentPrimary; shadowBlur: 0.3
                    }
                }
            }
        }

        // Stats Row
        Row {
            anchors.right: parent.right
            anchors.rightMargin: 10 * root.screenScale
            spacing: 30 * root.screenScale
            opacity: 0.6 // Kept at 0.6 as requested
            
            Row {
                spacing: 10 * root.screenScale
                visible: Sysinfo.weatherTempStr !== "--°C"
                Text {
                    text: Sysinfo.weatherTempStr
                    font.family: Theme.fontFamily
                    font.weight: Font.Bold
                    font.pixelSize: 24 * root.screenScale
                    color: "white"
                }
                Text { text: "🌡️"; font.pixelSize: 22 * root.screenScale; verticalAlignment: Text.AlignVCenter; opacity: 0.6 }
            }

            Row {
                spacing: 12 * root.screenScale
                visible: NetworkSpeed.downloadSpeed > 1024
                Text {
                    text: "↓ " + NetworkSpeed.downloadSpeedStr
                    font.family: Theme.fontFamily
                    font.weight: Font.Bold
                    font.pixelSize: 24 * root.screenScale
                    color: "white"
                }
                Text {
                    text: "↑ " + NetworkSpeed.uploadSpeedStr
                    font.family: Theme.fontFamily
                    font.weight: Font.Bold
                    font.pixelSize: 18 * root.screenScale
                    color: "white"
                    opacity: 0.5
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 3
                }
            }
        }

        // Holiday Badge
        Rectangle {
            visible: HolidayManager.todayHoliday !== ""
            anchors.right: parent.right
            width: holidayText.width + 30; height: 34; radius: 17
            color: "#1AFFFFFF"
            border.color: "#26FFFFFF"
            Text {
                id: holidayText
                anchors.centerIn: parent
                text: HolidayManager.todayHoliday
                font.family: Theme.fontFamily
                font.weight: Font.Bold
                font.pixelSize: 13 * root.screenScale
                color: Theme.accentSecondary
                font.letterSpacing: 1.0
                opacity: 0.7
            }
        }
    }
}
