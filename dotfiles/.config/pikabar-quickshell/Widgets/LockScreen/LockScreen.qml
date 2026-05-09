import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Effects
import Quickshell
import Quickshell.Wayland
import Quickshell.Services.Pam
import Quickshell.Io
import Quickshell.Widgets
import qs.Components
import qs.Settings
import qs.Services
import qs.Widgets.LockScreen
import "../../Helpers/Weather.js" as WeatherHelper

WlSessionLock {
    id: lock

    property string errorMessage: ""
    property bool authenticating: false
    property string password: ""
    property bool pamAvailable: typeof PamContext !== "undefined"
    property string weatherCity: Settings.settings.weatherCity
    property var weatherData: null
    property string weatherError: ""
    property string timeStr: Qt.formatDateTime(new Date(), "HH:mm")
    property string dateStr: Qt.formatDateTime(new Date(), "dddd, MMMM d")
    locked: false

    // Request to fetch weather with a little delay to ensure weatherCity is properly loaded.
    Component.onCompleted: {
        Qt.callLater(function () {
            fetchWeatherData();
        });
    }

    function fetchWeatherData() {
        if (!weatherCity) return;
        WeatherHelper.fetchCityWeather(weatherCity, function (result) {
            weatherData = result.weather;
            weatherError = "";
        }, function (err) {
            weatherError = err;
        });
    }

    function materialSymbolForCode(code) {
        if (code === 0) return "sunny";
        if (code === 1 || code === 2) return "partly_cloudy_day";
        if (code === 3) return "cloud";
        if (code >= 45 && code <= 48) return "foggy";
        if (code >= 51 && code <= 67) return "rainy";
        if (code >= 71 && code <= 77) return "weather_snowy";
        if (code >= 80 && code <= 82) return "rainy";
        if (code >= 95 && code <= 99) return "thunderstorm";
        return "cloud";
    }

    // Global timers moved to root to avoid duplication per monitor and potential race conditions
    Timer {
        id: clockTimer
        interval: 1000
        running: true
        repeat: true
        onTriggered: {
            lock.timeStr = Qt.formatDateTime(new Date(), "HH:mm");
            lock.dateStr = Qt.formatDateTime(new Date(), "dddd, MMMM d");
        }
    }

    Timer {
        id: weatherTimer
        interval: 600000 // 10 minutes
        running: true
        repeat: true
        onTriggered: fetchWeatherData()
    }

    function unlockAttempt() {
        if (!pamAvailable) {
            lock.errorMessage = "PAM authentication not available.";
            return;
        }
        if (!lock.password) {
            lock.errorMessage = "Password required.";
            return;
        }
        lock.authenticating = true;
        lock.errorMessage = "";

        // Use a more robust way to create PAM context
        var pam = Qt.createQmlObject('import Quickshell.Services.Pam; PamContext { config: "login"; user: "' + Quickshell.env("USER") + '" }', lock);
        
        const cleanup = () => {
            lock.authenticating = false;
            pam.destroy();
        };

        pam.onCompleted.connect(function (result) {
            if (result === PamResult.Success) {
                lock.locked = false;
                lock.password = "";
                lock.errorMessage = "";
            } else {
                lock.errorMessage = "Authentication failed.";
                lock.password = "";
            }
            cleanup();
        });

        pam.onError.connect(function (error) {
            lock.errorMessage = pam.message || "Authentication error.";
            lock.password = "";
            cleanup();
        });

        pam.onPamMessage.connect(function () {
            if (pam.messageIsError) {
                lock.errorMessage = pam.message;
            }
        });

        pam.onResponseRequiredChanged.connect(function () {
            if (pam.responseRequired && lock.authenticating) {
                pam.respond(lock.password);
            }
        });

        if (!pam.start()) {
            lock.errorMessage = "Failed to start PAM.";
            cleanup();
        }
    }

    WlSessionLockSurface {
        // Optimized background rendering
        Image {
            id: lockBgImage
            anchors.fill: parent
            fillMode: Image.PreserveAspectCrop
            source: WallpaperManager.currentWallpaper || ""
            cache: true
            smooth: true
            mipmap: false
            asynchronous: true
        }

        MultiEffect {
            id: lockBgBlur
            anchors.fill: parent
            source: lockBgImage
            blurEnabled: true
            blur: 0.48
            blurMax: 64 // Reduced from 128 for stability and performance
        }

        ColumnLayout {
            anchors.centerIn: parent
            spacing: 30
            width: Math.min(parent.width * 0.8, 400 * Theme.scale(Screen))

            Rectangle {
                Layout.alignment: Qt.AlignHCenter
                width: 80 * Theme.scale(Screen)
                height: 80 * Theme.scale(Screen)
                radius: 40
                color: Theme.accentPrimary

                Rectangle {
                    anchors.fill: parent
                    color: "transparent"
                    radius: 40
                    border.color: Theme.accentPrimary
                    border.width: 3 * Theme.scale(Screen)
                    z: 2
                }

                Avatar {}

                layer.enabled: true
                layer.effect: MultiEffect {
                    shadowEnabled: true
                    shadowColor: Theme.accentPrimary
                }
            }

            Text {
                Layout.alignment: Qt.AlignHCenter
                text: Quickshell.env("USER")
                font.family: Theme.fontFamily
                font.pixelSize: 24 * Theme.scale(Screen)
                font.weight: Font.Medium
                color: Theme.textPrimary
            }

            Rectangle {
                Layout.fillWidth: true
                height: 50 * Theme.scale(Screen)
                radius: 25
                color: Theme.surface
                opacity: passwordInput.activeFocus ? 0.8 : 0.3
                border.color: passwordInput.activeFocus ? Theme.accentPrimary : Theme.outline
                border.width: 2 * Theme.scale(Screen)

                TextInput {
                    id: passwordInput
                    anchors.fill: parent
                    anchors.margins: 15 * Theme.scale(Screen)
                    verticalAlignment: TextInput.AlignVCenter
                    horizontalAlignment: TextInput.AlignHCenter
                    font.family: Theme.fontFamily
                    font.pixelSize: 16 * Theme.scale(Screen)
                    color: Theme.textPrimary
                    echoMode: TextInput.Password
                    passwordCharacter: "●"
                    passwordMaskDelay: 0

                    text: lock.password
                    onTextChanged: lock.password = text

                    Text {
                        anchors.centerIn: parent
                        text: "Enter password..."
                        color: Theme.textSecondary
                        font.family: Theme.fontFamily
                        font.pixelSize: 16 * Theme.scale(Screen)
                        visible: !passwordInput.text && !passwordInput.activeFocus
                    }

                    Keys.onPressed: function (event) {
                        if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter) {
                            lock.unlockAttempt();
                        }
                    }

                    Component.onCompleted: forceActiveFocus()
                }
            }

            Rectangle {
                id: errorMessageRect
                Layout.alignment: Qt.AlignHCenter
                width: parent.width * 0.8
                height: 44 * Theme.scale(Screen)
                color: Theme.overlay
                radius: 18
                visible: lock.errorMessage !== ""

                Text {
                    anchors.centerIn: parent
                    text: lock.errorMessage
                    color: Theme.error
                    font.family: Theme.fontFamily
                    font.pixelSize: 14 * Theme.scale(Screen)
                    visible: lock.errorMessage !== ""
                }
            }

            Rectangle {
                Layout.alignment: Qt.AlignHCenter
                width: 120 * Theme.scale(Screen)
                height: 44 * Theme.scale(Screen)
                radius: 18
                opacity: (unlockButtonArea.containsMouse || lock.authenticating) ? 0.8 : 0.5
                color: unlockButtonArea.containsMouse ? Theme.accentPrimary : Theme.surface
                border.color: Theme.accentPrimary
                border.width: 2 * Theme.scale(Screen)
                enabled: !lock.authenticating

                Text {
                    id: unlockButtonText
                    anchors.centerIn: parent
                    text: lock.authenticating ? "..." : "Unlock"
                    font.family: Theme.fontFamily
                    font.pixelSize: 16 * Theme.scale(Screen)
                    font.bold: true
                    color: unlockButtonArea.containsMouse ? Theme.onAccent : Theme.accentPrimary
                }

                MouseArea {
                    id: unlockButtonArea
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: {
                        if (!lock.authenticating) {
                            lock.unlockAttempt();
                        }
                    }
                }

                Behavior on opacity { NumberAnimation { duration: 200 } }
            }
        }

        // Top info bar (Time/Date/Weather)
        Rectangle {
            width: infoColumn.width + 32 * Theme.scale(Screen)
            height: infoColumn.height + 8 * Theme.scale(Screen)
            color: Theme.backgroundPrimary || "#222"
            anchors.horizontalCenter: parent.horizontalCenter
            bottomLeftRadius: 20 * Theme.scale(Screen)
            bottomRightRadius: 20 * Theme.scale(Screen)

            ColumnLayout {
                id: infoColumn
                anchors.top: parent.top
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 8

                Text {
                    text: lock.timeStr
                    font.family: Theme.fontFamily
                    font.pixelSize: 48 * Theme.scale(Screen)
                    font.bold: true
                    color: Theme.textPrimary
                    Layout.alignment: Qt.AlignHCenter
                }
                Text {
                    text: lock.dateStr
                    font.family: Theme.fontFamily
                    font.pixelSize: 16 * Theme.scale(Screen)
                    color: Theme.textSecondary
                    opacity: 0.8
                    Layout.alignment: Qt.AlignHCenter
                }

                RowLayout {
                    spacing: 6
                    Layout.alignment: Qt.AlignHCenter
                    visible: weatherData && weatherData.current_weather

                    Text {
                        text: weatherData && weatherData.current_weather ? materialSymbolForCode(weatherData.current_weather.weathercode) : "cloud"
                        font.family: "Material Symbols Outlined"
                        font.pixelSize: 28 * Theme.scale(Screen)
                        color: Theme.accentPrimary
                    }

                    Text {
                        text: {
                            if (!weatherData || !weatherData.current_weather) return "--°C";
                            const temp = weatherData.current_weather.temperature;
                            const useF = Settings.settings.useFahrenheit || false;
                            return useF ? `${Math.round(temp * 9 / 5 + 32)}°F` : `${Math.round(temp)}°C`;
                        }
                        font.family: Theme.fontFamily
                        font.pixelSize: 18 * Theme.scale(Screen)
                        color: Theme.textSecondary
                    }
                }

                Text {
                    text: weatherError
                    color: Theme.error
                    visible: weatherError !== ""
                    font.family: Theme.fontFamily
                    font.pixelSize: 10 * Theme.scale(Screen)
                    Layout.alignment: Qt.AlignHCenter
                }
            }
        }

        // Bottom left bar (Battery)
        ColumnLayout {
            anchors.left: parent.left
            anchors.bottom: parent.bottom
            anchors.margins: 32
            spacing: 12
            BatteryCharge {}
        }

        // Bottom right bar (Power controls)
        ColumnLayout {
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: 32
            spacing: 12

            Repeater {
                model: [
                    { icon: "power_settings_new", cmd: ["shutdown", "-h", "now"], color: Theme.error },
                    { icon: "refresh", cmd: ["reboot"], color: Theme.accentPrimary },
                    { icon: "exit_to_app", cmd: ["loginctl", "terminate-user", Quickshell.env("USER")], color: Theme.accentSecondary }
                ]

                delegate: Rectangle {
                    width: 48 * Theme.scale(Screen)
                    height: 48 * Theme.scale(Screen)
                    radius: 24
                    color: area.containsMouse ? modelData.color : "transparent"
                    border.color: modelData.color
                    border.width: 1 * Theme.scale(Screen)

                    MouseArea {
                        id: area
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: Qt.createQmlObject('import Quickshell.Io; Process { command: ' + JSON.stringify(modelData.cmd) + '; running: true }', lock)
                    }

                    Text {
                        anchors.centerIn: parent
                        text: modelData.icon
                        font.family: "Material Symbols Outlined"
                        font.pixelSize: 24 * Theme.scale(Screen)
                        color: area.containsMouse ? Theme.onAccent : modelData.color
                    }
                }
            }
        }
    }
}
