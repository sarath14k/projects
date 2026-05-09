import QtQuick
import QtQuick.Effects
import QtMultimedia
import Qt.labs.folderlistmodel
import Quickshell
import qs.Services
import qs.Settings
import qs.Components

Item {
    id: root
    property var screen: null
    // Optimized: Use centralized Theme scaling
    readonly property real screenScale: Theme.scale(screen)

    // --- Local Player Logic ---
    property int currentTrackIndex: 0
    property url localMusicFolder: "file:///home/sarath/Music/NEFFEX"

    FolderListModel {
        id: musicModel
        folder: localMusicFolder
        showDirs: false
        sortField: FolderListModel.Name
    }

    MediaPlayer {
        id: internalPlayer
        audioOutput: AudioOutput { volume: 0.8 }
        source: (musicModel.count > 0) ? musicModel.get(currentTrackIndex, "fileURL") : ""
        
        onMediaStatusChanged: {
            if (mediaStatus === MediaPlayer.EndOfMedia) {
                root.nextTrack()
            }
        }
    }

    function togglePlay() {
        if (internalPlayer.playbackState === MediaPlayer.PlayingState) {
            internalPlayer.pause()
        } else if (musicModel.count > 0) {
            internalPlayer.play()
        }
    }

    function nextTrack() {
        if (musicModel.count > 0) {
            currentTrackIndex = (currentTrackIndex + 1) % musicModel.count
            internalPlayer.play()
        }
    }

    function prevTrack() {
        if (musicModel.count > 0) {
            currentTrackIndex = (currentTrackIndex - 1 + musicModel.count) % musicModel.count
            internalPlayer.play()
        }
    }

    width: 420 * screenScale
    height: 150 * screenScale
    visible: Settings.settings.showDesktopPlayer

    property string displayTitle: {
        if (musicModel.count <= 0) return "Scanning Jukebox...";
        var name = musicModel.get(currentTrackIndex, "fileName");
        if (!name) return "Loading...";
        return name.toString().replace(/\.[^/.]+$/, "");
    }
    
    property string displayArtist: "NEFFEX Collection"
    property bool activePlaying: internalPlayer.playbackState === MediaPlayer.PlayingState

    // GLOBAL SYNC FIX: Use a Binding with 'when' to prevent multiple monitors from overwriting each other
    Binding {
        target: Settings
        property: "localPlayerActive"
        value: true
        when: root.activePlaying
    }

    // Glass Background
    Rectangle {
        id: bg
        anchors.fill: parent
        radius: 20 * screenScale
        color: "#1A000000"
        border.color: "#26FFFFFF"
        border.width: 1
        
        layer.enabled: true
        layer.effect: MultiEffect {
            blurEnabled: true
            blur: 1.0 // MAXIMUM FROSTED BLUR
            shadowEnabled: true
            shadowColor: "#B3000000"
            shadowBlur: 0.8
        }
    }

    Row {
        id: playerContent
        anchors.centerIn: parent
        spacing: 20 * screenScale

        // Album Art Icon
        Rectangle {
            width: 90 * screenScale
            height: 90 * screenScale
            radius: 15 * screenScale
            color: "#1AFFFFFF"
            border.color: "#1AFFFFFF"
            border.width: 1
            
            Text {
                anchors.centerIn: parent
                text: "music_note"
                font.family: "Material Symbols Outlined"
                font.pixelSize: 45 * screenScale
                color: Theme.accentPrimary
                opacity: activePlaying ? 0.9 : 0.4
                
                Behavior on opacity { NumberAnimation { duration: 500 } }
            }
        }

        // Info & Controls
        Column {
            spacing: 12 * screenScale
            width: 270 * screenScale
            anchors.verticalCenter: parent.verticalCenter

            Column {
                width: parent.width
                spacing: 2
                
                Text {
                    text: "NOW PLAYING"
                    font.family: Theme.fontFamily
                    font.pixelSize: 10 * screenScale
                    font.weight: Font.Black
                    color: "white"
                    opacity: 0.5
                    font.letterSpacing: 3.0
                }
                
                Text {
                    width: parent.width
                    text: root.displayTitle
                    font.family: Theme.fontFamily
                    font.weight: Font.Bold
                    font.pixelSize: 20 * screenScale
                    color: "white"
                    elide: Text.ElideRight
                }
                Text {
                    width: parent.width
                    text: root.displayArtist
                    font.family: Theme.fontFamily
                    font.pixelSize: 13 * screenScale
                    color: "white"
                    opacity: 0.6
                    elide: Text.ElideRight
                }
            }

            Row {
                spacing: 25 * screenScale
                anchors.horizontalCenter: parent.horizontalCenter

                IconButton {
                    icon: "skip_previous"
                    size: 36 * screenScale
                    onClicked: root.prevTrack()
                }

                IconButton {
                    icon: root.activePlaying ? "pause_circle" : "play_circle"
                    size: 54 * screenScale
                    onClicked: root.togglePlay()
                }

                IconButton {
                    icon: "skip_next"
                    size: 36 * screenScale
                    onClicked: root.nextTrack()
                }
            }
        }
    }

    Behavior on opacity { NumberAnimation { duration: 500 } }
}
