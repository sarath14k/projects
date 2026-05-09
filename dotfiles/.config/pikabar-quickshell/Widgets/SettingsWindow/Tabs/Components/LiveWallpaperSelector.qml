import QtQuick
import QtQuick.Controls
import QtQuick.Effects
import QtQuick.Layouts
import QtMultimedia
import qs.Components
import qs.Services
import qs.Settings

Rectangle {
    id: wallpaperOverlay
    focus: true

    // Function to show the overlay and load wallpapers
    function show() {
        // Ensure wallpapers are loaded
        WallpaperManager.loadWallpapers();
        wallpaperOverlay.visible = true;
        wallpaperOverlay.forceActiveFocus();
    }

    // Function to hide the overlay
    function hide() {
        wallpaperOverlay.visible = false;
    }

    color: Theme.backgroundPrimary
    visible: false
    z: 1000

    // Handle escape key to close
    Keys.onPressed: function(event) {
        if (event.key === Qt.Key_Escape) {
            wallpaperOverlay.hide();
            event.accepted = true;
        }
    }

    // Click outside to close
    MouseArea {
        anchors.fill: parent
        onClicked: {
            wallpaperOverlay.hide();
        }
    }

    // Content area that stops event propagation
    MouseArea {
        anchors.fill: parent
        anchors.margins: 24
        onClicked: {}

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            // Wallpaper Grid
            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                ScrollView {
                    anchors.fill: parent
                    clip: true
                    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                    ScrollBar.vertical.policy: ScrollBar.AsNeeded

                    GridView {
                        id: wallpaperGrid

                        anchors.fill: parent
                        cellWidth: Math.max(120 * Theme.scale(screen), (parent.width / 3) - 12 * Theme.scale(screen))
                        cellHeight: cellWidth * 0.6
                        model: WallpaperManager.videoList
                        cacheBuffer: 64
                        leftMargin: 8
                        rightMargin: 8
                        topMargin: 8
                        bottomMargin: 8

                        delegate: Item {
                            width: wallpaperGrid.cellWidth - 8 * Theme.scale(screen)
                            height: wallpaperGrid.cellHeight - 8 * Theme.scale(screen)

                            Rectangle {
                                id: wallpaperItem

                                anchors.fill: parent
                                anchors.margins: 3
                                color: Theme.surface
                                radius: 12
                                border.color: Settings.settings.liveWallpaperPath === modelData ? Theme.accentPrimary : Theme.outline
                                border.width: 2 * Theme.scale(screen)

                                MediaPlayer {
                                    id: player
                                    source: "file://" + modelData
                                    loops: MediaPlayer.Infinite
                                    videoOutput: videoOutput
                                }

                                VideoOutput {
                                    id: videoOutput
                                    anchors.fill: parent
                                    anchors.margins: 2
                                    fillMode: VideoOutput.PreserveAspectCrop
                                    opacity: player.playbackState === MediaPlayer.PlayingState ? 1 : 0.6
                                    
                                    Behavior on opacity {
                                        NumberAnimation { duration: 300 }
                                    }

                                    layer.enabled: true
                                    layer.effect: MultiEffect {
                                        maskEnabled: true
                                        maskSource: mask
                                    }
                                }

                                Item {
                                    id: mask
                                    anchors.fill: videoOutput
                                    layer.enabled: true
                                    visible: false
                                    Rectangle {
                                        width: videoOutput.width
                                        height: videoOutput.height
                                        radius: 12
                                    }
                                }

                                // Filename label
                                Rectangle {
                                    anchors {
                                        bottom: parent.bottom
                                        left: parent.left
                                        right: parent.right
                                        margins: 6
                                    }
                                    height: 20
                                    color: "#aa000000"
                                    radius: 4
                                    visible: player.playbackState !== MediaPlayer.PlayingState

                                    Text {
                                        anchors.centerIn: parent
                                        width: parent.width - 8
                                        text: modelData.split('/').pop()
                                        color: "white"
                                        font.pixelSize: 10
                                        elide: Text.ElideMiddle
                                        horizontalAlignment: Text.AlignHCenter
                                    }
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    hoverEnabled: true
                                    cursorShape: Qt.PointingHandCursor
                                    onEntered: player.play()
                                    onExited: {
                                        player.stop()
                                    }
                                    onClicked: {
                                        WallpaperManager.changeLiveWallpaper(modelData);
                                        wallpaperOverlay.hide();
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
