import QtQuick
import QtQuick.Effects
import Quickshell
import qs.Services
import qs.Settings
import qs.Components

Item {
    id: root
    property var screen: null
    
    // Optimized: Use centralized Theme scaling
    readonly property real screenScale: Theme.scale(screen)
    
    // Explicitly reactive playback detection
    readonly property bool isPlaying: MusicManager.isPlaying || Settings.localPlayerActive
    
    // Layout: Half-width and 12% screen height (slight increase for better visibility)
    width: parent.width * 0.5
    height: parent.height * 0.12
    
    anchors.horizontalCenter: parent.horizontalCenter

    Cava {
        id: cava
        count: 30
        noiseReduction: 85
        active: root.isPlaying
    }

    // Blurred background tray
    Rectangle {
        anchors.fill: parent
        anchors.margins: 10 * screenScale
        radius: 30 * screenScale
        color: "#0D000000"
        opacity: root.isPlaying ? 1.0 : 0.0
        
        layer.enabled: true
        layer.effect: MultiEffect {
            blurEnabled: true
            blur: 0.8
        }
        
        Behavior on opacity { NumberAnimation { duration: 500 } }
    }

    Row {
        id: barsRow
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        width: parent.width * 0.98
        height: parent.height - 10 * screenScale
        spacing: 4 * screenScale
        
        // Left Side Bars (0-14)
        Repeater {
            model: 15
            Rectangle {
                width: (barsRow.width - playerGap.width) / 30 - barsRow.spacing
                height: Math.max(6, cava.values[index] * barsRow.height)
                radius: width / 2
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#4B0082" }
                    GradientStop { position: 0.3; color: "#00D2FF" }
                    GradientStop { position: 0.7; color: "#3BFF9D" }
                    GradientStop { position: 1.0; color: "#FF007F" }
                }
                opacity: 0.4
                anchors.bottom: parent.bottom
                Behavior on height { NumberAnimation { duration: 150; easing.type: Easing.OutCubic } }
            }
        }

        // The Gap for the Player
        Item {
            id: playerGap
            width: 440 * screenScale // Match player width + small margin
            height: 1
        }

        // Right Side Bars (15-29)
        Repeater {
            model: 15
            Rectangle {
                width: (barsRow.width - playerGap.width) / 30 - barsRow.spacing
                height: Math.max(6, cava.values[index + 15] * barsRow.height)
                radius: width / 2
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#4B0082" }
                    GradientStop { position: 0.3; color: "#00D2FF" }
                    GradientStop { position: 0.7; color: "#3BFF9D" }
                    GradientStop { position: 1.0; color: "#FF007F" }
                }
                opacity: 0.4
                anchors.bottom: parent.bottom
                Behavior on height { NumberAnimation { duration: 150; easing.type: Easing.OutCubic } }
            }
        }
        
        layer.enabled: true
        layer.effect: MultiEffect {
            blurEnabled: true
            blur: 0.1
            shadowEnabled: true
            shadowColor: "#FFFFFF"
            shadowBlur: 0.5
        }
    }
    
    visible: isPlaying
    opacity: visible ? 1.0 : 0.0
    Behavior on opacity { NumberAnimation { duration: 1000 } }
}
