import QtQuick
import Quickshell
import Quickshell.Wayland
import qs.Services
import qs.Settings

ShellRoot {
    property string wallpaperSource: WallpaperManager.currentWallpaper !== "" && !Settings.settings.useSWWW ? WallpaperManager.currentWallpaper : ""

    Variants {
        model: Quickshell.screens

        PanelWindow {
            required property ShellScreen modelData

            visible: wallpaperSource !== ""
            anchors {
                bottom: true
                top: true
                right: true
                left: true
            }
            margins {
                top: 0
            }
            color: "transparent"
            screen: modelData
            WlrLayershell.layer: WlrLayer.Background
            WlrLayershell.exclusionMode: ExclusionMode.Ignore
            WlrLayershell.namespace: "quickshell-wallpaper"
            Image {
                anchors.fill: parent
                fillMode: Image.PreserveAspectCrop
                source: wallpaperSource
                visible: wallpaperSource !== ""
                cache: true
                smooth: true
                mipmap: false
            }

            DesktopClock {
                id: desktopClock
                screen: modelData
                anchors {
                    top: parent.top
                    right: parent.right
                    topMargin: 100 * (modelData.width / 2560)
                    rightMargin: 100 * (modelData.width / 2560)
                }
                visible: Settings.settings.showDesktopClock
            }

            DesktopPlayer {
                id: player
                screen: modelData
                anchors.centerIn: cava
                anchors.verticalCenterOffset: 20 * (modelData.width / 2560)
            }

            DesktopCava {
                id: cava
                screen: modelData
                anchors.bottom: parent.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottomMargin: 40 * (modelData.width / 2560)
            }
        }
    }


}