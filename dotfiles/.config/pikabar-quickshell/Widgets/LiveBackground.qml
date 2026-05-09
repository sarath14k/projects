import QtQuick
import QtQuick.Effects
import QtMultimedia
import Quickshell
import Quickshell.Wayland
import Quickshell.Hyprland
import qs.Services
import qs.Settings

ShellRoot {
    id: root
    property bool locked: false
    property bool panelsOpen: false
    property bool isFullscreen: false
    property bool hasWindows: false
    property int currentHour: new Date().getHours()

    // 1. Fullscreen & Window Detection (Checks every 3 seconds)
    Timer {
        interval: 3000
        running: Settings.settings.pauseOnFullscreen || Settings.settings.focusModeBlur || Settings.settings.uiEmphasis
        repeat: true
        triggeredOnStart: true
        onTriggered: {
            const activeWs = Hyprland.activeWorkspace;
            if (activeWs) {
                isFullscreen = activeWs.fullscreen;
                hasWindows = activeWs.clients.length > 0;
            }
            currentHour = new Date().getHours();
        }
    }

    // 2. Idle Detection - Removed (unsupported module)

    // 3. Weather Sync Logic
    Connections {
        target: Sysinfo
        enabled: Settings.settings.weatherSync
        function onWeatherTempStrChanged() {
            if (!Settings.settings.weatherSync) return;
            
            let condition = Sysinfo.weatherTempStr.toLowerCase();
            let folder = Settings.settings.wallpaperFolder;
            
            if (condition.includes("rain") || condition.includes("drizzle")) {
                Settings.settings.liveWallpaperPath = folder + "/hydrangeas-rain.3840x2160.mp4";
            } else if (condition.includes("cloud") || condition.includes("mist")) {
                Settings.settings.liveWallpaperPath = folder + "/mist-over-the-pines.3840x2160.mp4";
            } else if (condition.includes("clear") || condition.includes("sunny")) {
                Settings.settings.liveWallpaperPath = folder + "/mount-fujiyama.3840x2160.mp4";
            }
        }
    }

    Variants {
        model: Quickshell.screens

        PanelWindow {
            required property ShellScreen modelData
            
            anchors {
                bottom: true
                top: true
                right: true
                left: true
            }
            color: "transparent"
            screen: modelData
            WlrLayershell.layer: WlrLayer.Background
            WlrLayershell.exclusionMode: ExclusionMode.Ignore
            WlrLayershell.namespace: "quickshell-wallpaper"
            visible: Settings.settings.useLiveWallpaper

            MediaPlayer {
                id: mediaPlayer
                source: {
                    let path = Settings.settings.liveWallpaperPath;
                    if (Settings.settings.limitLiveWallpaperRes) {
                        let optimized = path.replace(".3840x2160", ".1080p").replace(".4k", ".1080p");
                        if (optimized !== path) return "file:///" + optimized;
                    }
                    return "file:///" + path;
                }
                loops: MediaPlayer.Infinite
                audioOutput: null
                videoOutput: videoOutput

                function updatePlayback() {
                    let shouldPause = locked || 
                                     (Settings.settings.pauseOnFullscreen && root.isFullscreen);
                    
                    if (Settings.settings.useLiveWallpaper && !shouldPause) {
                        mediaPlayer.play();
                    } else {
                        mediaPlayer.pause();
                    }
                }

                Component.onCompleted: updatePlayback()
                onSourceChanged: updatePlayback()
                
                onMediaStatusChanged: {
                    if (mediaStatus === MediaPlayer.ErrorStatus && Settings.settings.limitLiveWallpaperRes) {
                        source = "file:///" + Settings.settings.liveWallpaperPath;
                        updatePlayback();
                    }
                }
            }

            // Sync playback with external states
            Connections {
                target: root
                function onLockedChanged() { mediaPlayer.updatePlayback() }
                function onIsFullscreenChanged() { mediaPlayer.updatePlayback() }
            }

            Connections {
                target: Settings.settings
                function onUseLiveWallpaperChanged() { mediaPlayer.updatePlayback() }
                function onLiveWallpaperPathChanged() { mediaPlayer.updatePlayback() }
                function onLimitLiveWallpaperResChanged() { mediaPlayer.updatePlayback() }
            }

            VideoOutput {
                id: videoOutput
                anchors.fill: parent
                fillMode: VideoOutput.PreserveAspectCrop
                
                // Double-click to switch wallpaper
                MouseArea {
                    anchors.fill: parent
                    enabled: Settings.settings.doubleClickSwitch
                    onDoubleClicked: WallpaperManager.setNextWallpaper()
                }
                
                layer.enabled: (Settings.settings.focusModeBlur && root.hasWindows) || 
                              (Settings.settings.uiEmphasis && root.panelsOpen) ||
                              Settings.settings.dynamicColorShift
                
                layer.effect: MultiEffect {
                    // Blur logic: strongest when panels are open, medium when windows are open
                    blurEnabled: true
                    blur: (Settings.settings.uiEmphasis && root.panelsOpen) ? 0.8 : 
                          (Settings.settings.focusModeBlur && root.hasWindows) ? 0.4 : 0.0
                    
                    // Saturation logic: softer at night
                    saturation: (Settings.settings.dynamicColorShift && (root.currentHour >= 20 || root.currentHour <= 6)) ? -0.4 : 0.0
                    
                    // Colorization: subtle warmth at night
                    colorization: (Settings.settings.dynamicColorShift && (root.currentHour >= 20 || root.currentHour <= 6)) ? 0.15 : 0.0
                    colorizationColor: "#ffaa00"
                }
                
                // Night mode & UI Emphasis dimming
                opacity: {
                    let base = 1.0;
                    if (Settings.settings.uiEmphasis && root.panelsOpen) base -= 0.3;
                    if (Settings.settings.nightModeDim && (root.currentHour >= 20 || root.currentHour <= 6)) base -= 0.2;
                    return Math.max(0.4, base);
                }
                
                Behavior on opacity { NumberAnimation { duration: 500 } }
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
                anchors.bottomMargin: 40 * (modelData.width / 2560)
            }
        }
    }
}
