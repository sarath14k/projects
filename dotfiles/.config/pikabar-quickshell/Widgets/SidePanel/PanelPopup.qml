import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import Quickshell
import Quickshell.Io
import Quickshell.Wayland
import qs.Components
import qs.Settings
import qs.Widgets.SettingsWindow

PanelWithOverlay {
    id: sidebarPopup

    property var shell: null

    function showAt() {
        sidebarPopupRect.showAt();
    }

    function hidePopup() {
        sidebarPopupRect.hidePopup();
    }

    function show() {
        sidebarPopupRect.showAt();
    }

    function dismiss() {
        sidebarPopupRect.hidePopup();
    }

    // Trigger initial weather loading when component is completed
    Component.onCompleted: {
        // Load initial weather data after a short delay to ensure all components are ready
        Qt.callLater(function() {
            if (weather && weather.fetchCityWeather)
                weather.fetchCityWeather();

        });
    }

    Rectangle {
        // Access the shell's SettingsWindow instead of creating a new one
        id: sidebarPopupRect

        property real slideOffset: width
        property bool isAnimating: false
        property int leftPadding: 20 * Theme.scale(screen)
        property int bottomPadding: 20 * Theme.scale(screen)
        // Recording properties
        property bool isRecording: false

        function checkRecordingStatus() {
            if (isRecording)
                checkRecordingProcess.running = true;

        }

        function showAt() {
            if (!sidebarPopup.visible) {
                sidebarPopup.visible = true;
                forceActiveFocus();
                slideAnim.from = width;
                slideAnim.to = 0;
                slideAnim.running = true;
                if (weather)
                    weather.startWeatherFetch();

                if (systemWidget)
                    systemWidget.panelVisible = true;

            }
        }

        function hidePopup() {
            if (shell && shell.settingsWindow && shell.settingsWindow.visible)
                shell.settingsWindow.visible = false;

            if (sidebarPopup.visible) {
                slideAnim.from = 0;
                slideAnim.to = width;
                slideAnim.running = true;
            }
        }

        // Start screen recording using Quickshell.execDetached
        function startRecording() {
            var currentDate = new Date();
            var hours = String(currentDate.getHours()).padStart(2, '0');
            var minutes = String(currentDate.getMinutes()).padStart(2, '0');
            var day = String(currentDate.getDate()).padStart(2, '0');
            var month = String(currentDate.getMonth() + 1).padStart(2, '0');
            var year = currentDate.getFullYear();
            var filename = hours + "-" + minutes + "-" + day + "-" + month + "-" + year + ".mp4";
            var videoPath = Settings.settings.videoPath;
            if (videoPath && !videoPath.endsWith("/"))
                videoPath += "/";

            var outputPath = videoPath + filename;
            var command = "gpu-screen-recorder -w portal" + " -f " + Settings.settings.recordingFrameRate + " -a default_output" + " -k " + Settings.settings.recordingCodec + " -ac " + Settings.settings.audioCodec + " -q " + Settings.settings.recordingQuality + " -cursor " + (Settings.settings.showCursor ? "yes" : "no") + " -cr " + Settings.settings.colorRange + " -o " + outputPath;
            Quickshell.execDetached(["sh", "-c", command]);
            isRecording = true;
        }

        // Stop recording using Quickshell.execDetached
        function stopRecording() {
            Quickshell.execDetached(["sh", "-c", "pkill -SIGINT -f 'gpu-screen-recorder.*portal'"]);
            // Optionally, force kill after a delay
            var cleanupTimer = Qt.createQmlObject('import QtQuick; Timer { interval: 3000; running: true; repeat: false }', sidebarPopupRect);
            cleanupTimer.triggered.connect(function() {
                Quickshell.execDetached(["sh", "-c", "pkill -9 -f 'gpu-screen-recorder.*portal' 2>/dev/null || true"]);
                cleanupTimer.destroy();
            });
            isRecording = false;
        }

        width: 480 * Theme.scale(screen)
        height: 660 * Theme.scale(screen)
        visible: parent.visible
        color: "transparent"
        anchors.top: parent.top
        anchors.right: parent.right
        // Clean up processes on destruction
        Component.onDestruction: {
            if (isRecording)
                stopRecording();

        }

        Process {
            id: checkRecordingProcess

            command: ["pgrep", "-f", "gpu-screen-recorder.*portal"]
            onExited: function(exitCode, exitStatus) {
                var isActuallyRecording = exitCode === 0;
                if (isRecording && !isActuallyRecording)
                    isRecording = isActuallyRecording;

            }
        }

        // Prevent closing when clicking in the panel bg
        MouseArea {
            anchors.fill: parent
        }

        NumberAnimation {
            id: slideAnim

            target: sidebarPopupRect
            property: "slideOffset"
            duration: 300
            easing.type: Easing.OutCubic
            onStopped: {
                if (sidebarPopupRect.slideOffset === sidebarPopupRect.width) {
                    sidebarPopup.visible = false;
                    if (weather)
                        weather.stopWeatherFetch();

                    if (systemWidget)
                        systemWidget.panelVisible = false;

                }
                sidebarPopupRect.isAnimating = false;
            }
            onStarted: {
                sidebarPopupRect.isAnimating = true;
            }
        }

        Rectangle {
            id: mainRectangle

            // anchors.top: sidebarPopupRect.top
            width: sidebarPopupRect.width - sidebarPopupRect.leftPadding
            height: sidebarPopupRect.height - sidebarPopupRect.bottomPadding
            x: sidebarPopupRect.leftPadding + sidebarPopupRect.slideOffset
            y: 0
            color: Theme.backgroundPrimary
            bottomLeftRadius: 20

            Behavior on x {
                enabled: !sidebarPopupRect.isAnimating

                NumberAnimation {
                    duration: 300
                    easing.type: Easing.OutCubic
                }

            }

        }

        // SettingsIcon component
        SettingsIcon {
            id: settingsModal

            onWeatherRefreshRequested: {
                if (weather && weather.fetchCityWeather)
                    weather.fetchCityWeather();

            }
        }

        Item {
            anchors.fill: mainRectangle
            x: sidebarPopupRect.slideOffset
            Keys.onEscapePressed: sidebarPopupRect.hidePopup()

            Flickable {
                anchors.fill: parent
                contentHeight: mainLayout.implicitHeight + 40 * Theme.scale(screen)
                clip: true
                boundsBehavior: Flickable.StopAtBounds
                ScrollBar.vertical: ScrollBar {
                    width: 4 * Theme.scale(screen)
                    policy: ScrollBar.AsNeeded
                }

                ColumnLayout {
                    id: mainLayout
                    width: parent.width - 20 * Theme.scale(screen)
                    anchors.horizontalCenter: parent.horizontalCenter
                    spacing: 12 * Theme.scale(screen)

                    System {
                        id: systemWidget
                        width: parent.width
                        height: 80 * Theme.scale(screen)
                        settingsModal: settingsModal
                        Layout.alignment: Qt.AlignHCenter
                    }

                    Weather {
                        id: weather
                        width: parent.width
                        height: 180 * Theme.scale(screen)
                        Layout.alignment: Qt.AlignHCenter
                    }

                    // Music and System Monitor row
                    RowLayout {
                        spacing: 12 * Theme.scale(screen)
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter

                        Music {
                            Layout.preferredWidth: 320 * Theme.scale(screen)
                            height: 250 * Theme.scale(screen)
                        }

                        SystemMonitor {
                            id: systemMonitor
                            Layout.fillWidth: true
                            height: 250 * Theme.scale(screen)
                        }
                    }

                    SensorsView {
                        id: sensorsView
                        Layout.fillWidth: true
                        show: systemMonitor.showDetails
                    }

                    RowLayout {
                        spacing: 12 * Theme.scale(screen)
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter

                        PowerProfile {
                            Layout.fillWidth: true
                            height: 70 * Theme.scale(screen)
                        }

                        Shortcuts {
                            Layout.fillWidth: true
                            height: 70 * Theme.scale(screen)
                        }
                    }

                    Rectangle {
                        height: 20 * Theme.scale(screen)
                        color: "transparent"
                        Layout.fillWidth: true
                    }
                }
            }

            Behavior on x {
                enabled: !sidebarPopupRect.isAnimating

                NumberAnimation {
                    duration: 300
                    easing.type: Easing.OutCubic
                }

            }

        }

    }

}
