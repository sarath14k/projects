pragma Singleton
import QtQuick
import Qt.labs.folderlistmodel
import Quickshell
import Quickshell.Io
import qs.Settings

Singleton {
    id: manager

    Item {
        Component.onCompleted: {
            loadWallpapers();
            setCurrentWallpaper(currentWallpaper, true);
            toggleRandomWallpaper();
        }
    }

    property var wallpaperList: []
    property var videoList: []
    property string currentWallpaper: Settings.settings.currentWallpaper
    property bool scanning: false
    property string transitionType: Settings.settings.transitionType
    property var randomChoices: ["fade", "left", "right", "top", "bottom", "wipe", "wave", "grow", "center", "any", "outer"]

    function loadWallpapers() {
        scanning = true;
        wallpaperList = [];
        videoList = [];
        folderModel.folder = "";
        folderModel.folder = "file://" + (Settings.settings.wallpaperFolder !== undefined ? Settings.settings.wallpaperFolder : "");
        videoModel.folder = "";
        videoModel.folder = "file://" + (Settings.settings.wallpaperFolder !== undefined ? Settings.settings.wallpaperFolder : "");
    }

    function changeWallpaper(path) {
        setCurrentWallpaper(path);
    }

    function changeLiveWallpaper(path) {
        Settings.settings.liveWallpaperPath = path;
    }

    function setCurrentWallpaper(path, isInitial) {
        currentWallpaper = path;
        if (!isInitial) {
            Settings.settings.currentWallpaper = path;
        }
        if (Settings.settings.useSWWW) {
            if (Settings.settings.transitionType === "random") {
                transitionType = randomChoices[Math.floor(Math.random() * randomChoices.length)];
            } else {
                transitionType = Settings.settings.transitionType;
            }
            changeWallpaperProcess.running = true;
        }

        if (randomWallpaperTimer.running) {
            randomWallpaperTimer.restart();
        }

        generateTheme();
    }

    property int currentVideoIndex: 0
    property int currentImageIndex: 0

    function setNextWallpaper() {
        // Live Wallpapers
        if (Settings.settings.useLiveWallpaper && Settings.settings.randomLiveWallpaper && videoList.length > 0) {
            let originals = videoList.filter(path => !path.includes(".1080p"));
            if (originals.length > 0) {
                // Find current index if not set
                if (currentVideoIndex < 0) currentVideoIndex = originals.indexOf(Settings.settings.liveWallpaperPath);
                
                currentVideoIndex = (currentVideoIndex + 1) % originals.length;
                let nextPath = originals[currentVideoIndex];
                if (nextPath) Settings.settings.liveWallpaperPath = nextPath;
            }
        }

        // Static Wallpapers
        if (Settings.settings.randomWallpaper && wallpaperList.length > 0) {
            if (currentImageIndex < 0) currentImageIndex = wallpaperList.indexOf(currentWallpaper);
            
            currentImageIndex = (currentImageIndex + 1) % wallpaperList.length;
            let nextPath = wallpaperList[currentImageIndex];
            if (nextPath) setCurrentWallpaper(nextPath);
        }
    }

    function toggleRandomWallpaper() {
        const anyRandom = Settings.settings.randomWallpaper || Settings.settings.randomLiveWallpaper;
        if (anyRandom) {
            if (!randomWallpaperTimer.running) {
                randomWallpaperTimer.start();
                setNextWallpaper();
            }
        } else {
            randomWallpaperTimer.stop();
        }
    }
    
    function restartRandomWallpaperTimer() {
        if (Settings.settings.randomWallpaper) {
            randomWallpaperTimer.stop();
            randomWallpaperTimer.start();
        }
    }

    function generateTheme() {
        if (Settings.settings.useWallpaperTheme) {
            generateThemeProcess.running = true;
        }
    }

    Timer {
        id: randomWallpaperTimer
        interval: Settings.settings.wallpaperInterval * 1000
        running: false
        repeat: true
        onTriggered: setNextWallpaper()
        triggeredOnStart: false
    }

    FolderListModel {
        id: folderModel
        // Swww supports many images format but Quickshell only support a subset of those.
        nameFilters: ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.pnm", "*.bmp"]
        showDirs: false
        sortField: FolderListModel.Name
        onStatusChanged: {
            if (status === FolderListModel.Ready) {
                var files = [];
                for (var i = 0; i < count; i++) {
                    var filepath = (Settings.settings.wallpaperFolder !== undefined ? Settings.settings.wallpaperFolder : "") + "/" + get(i, "fileName");
                    files.push(filepath);
                }
                wallpaperList = files;
                scanning = false;
            }
        }
    }

    FolderListModel {
        id: videoModel
        nameFilters: ["*.mp4", "*.mkv", "*.webm", "*.mov"]
        showDirs: false
        sortField: FolderListModel.Name
        onStatusChanged: {
            if (status === FolderListModel.Ready) {
                var files = [];
                for (var i = 0; i < count; i++) {
                    var filepath = (Settings.settings.wallpaperFolder !== undefined ? Settings.settings.wallpaperFolder : "") + "/" + get(i, "fileName");
                    files.push(filepath);
                }
                videoList = files;
                scanning = false;
            }
        }
    }

    Process {
        id: changeWallpaperProcess
        command: ["swww", "img", "--resize", Settings.settings.wallpaperResize, "--transition-fps", Settings.settings.transitionFps.toString(), "--transition-type", transitionType, "--transition-duration", Settings.settings.transitionDuration.toString(), currentWallpaper]
        running: false
    }
    
    Process {
        id: generateThemeProcess
        command: ["wallust", "run", currentWallpaper, "-u", "-k", "-d", "Templates"]
        workingDirectory: Quickshell.shellDir
        running: false
    }
}
