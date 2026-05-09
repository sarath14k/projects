pragma Singleton
import QtQuick
import Qt.labs.folderlistmodel
import Quickshell
import Quickshell.Io
import "../Helpers/Weather.js" as WeatherHelper

Singleton {
    id: manager

    property string weatherCity: "" // Set from outside to break circular dependency
    property string updateInterval: "2s"
    property string cpuUsageStr: ""
    property string cpuTempStr: ""
    property string memoryUsageStr: ""
    property string memoryUsagePerStr: ""
    property real cpuUsage: 0
    property real memoryUsage: 0
    property real cpuTemp: 0
    property real diskUsage: 0
    property real memoryUsagePer: 0
    property string diskUsageStr: ""

    property var allSensors: ({})

    property string gpuTempStr: ""
    property string gpuMemUsageStr: ""
    property real gpuTemp: 0
    property real gpuMemUsed: 0

    property string roomTempStr: "--°C"
    property real roomTemp: 0
    property string weatherTempStr: "--°C"
    property real weatherTemp: 0
    property double lastWeatherAttempt: 0
    property bool weatherFetching: false

    Timer {
        id: sensorTimer
        interval: 5000
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: sensorProcess.running = true
    }

    Process {
        id: sensorProcess
        command: ["python3", Quickshell.shellDir + "/scripts/sys_temps.py", "--json"]
        stdout: StdioCollector {
            onStreamFinished: {
                try {
                    const data = JSON.parse(text);
                    
                    // 1. CPU Temp
                    if (data["AMD CPU"]) {
                        const pkg = data["AMD CPU"].find(t => t.label === "Package (Tctl)");
                        if (pkg) {
                            cpuTemp = pkg.value;
                            cpuTempStr = pkg.value.toFixed(1) + "°C";
                        }
                    }

                    // 2. GPU Temp
                    if (data["AMD GPU"]) {
                        const edge = data["AMD GPU"].find(t => t.label === "Edge");
                        if (edge) {
                            // Exponential Moving Average (EMA) for fluid transitions
                            // Formula: NewAvg = (Alpha * Current) + ((1 - Alpha) * OldAvg)
                            const alpha = 0.3; // Snappiness factor
                            
                            if (gpuTemp === 0) {
                                gpuTemp = edge.value; // Initialize
                            } else {
                                gpuTemp = (alpha * edge.value) + ((1 - alpha) * gpuTemp);
                            }
                            
                            gpuTempStr = gpuTemp.toFixed(1) + "°C";
                            edge.value = gpuTemp; // Update global data for sensors view
                        }
                    }

                    allSensors = data;

                    // 3. Ambient Temp (Local Sensor)
                    if (data["ACPI (Ambient)"]) {
                        const amb = data["ACPI (Ambient)"].find(t => t.label === "Ambient");
                        if (amb) {
                            roomTemp = amb.value;
                            roomTempStr = amb.value.toFixed(1) + "°C";
                        }
                    }

                    // Always trigger weather update if it's missing, but it's now separate
                    updateWeatherTemp();
                } catch (e) {
                    console.error("Failed to parse sensor JSON:", e);
                }
            }
        }
    }

    function updateWeatherTemp() {
        const now = Date.now();
        // If we don't have weather data, retry every 2 minutes. If we do, update every 30 minutes.
        const cooldown = (weatherTempStr === "--°C") ? 120000 : 1800000;

        if (weatherCity && Network.hasActiveConnection && !weatherFetching && (now - lastWeatherAttempt > cooldown)) {
            lastWeatherAttempt = now;
            weatherFetching = true;
            geoProcess.running = true;
        }
    }

    onWeatherCityChanged: {
        updateWeatherTemp();
    }

    Component.onCompleted: {
        updateWeatherTemp();
    }

    Process {
        id: geoProcess
        command: ["curl", "-s", "--connect-timeout", "3", "--max-time", "5", "https://geocoding-api.open-meteo.com/v1/search?name=" + encodeURIComponent(weatherCity) + "&count=1"]
        stdout: StdioCollector {
            onStreamFinished: {
                try {
                    const data = JSON.parse(text);
                    if (data.results && data.results.length > 0) {
                        weatherTempProcess.command = [
                            "curl", "-s", "--connect-timeout", "3", "--max-time", "5",
                            "https://api.open-meteo.com/v1/forecast?latitude=" + data.results[0].latitude + 
                            "&longitude=" + data.results[0].longitude + "&current_weather=true"
                        ];
                        weatherTempProcess.running = true;
                    }
                } catch (e) {
                    weatherFetching = false;
                }
            }
        }
    }

    Process {
        id: weatherTempProcess
        stdout: StdioCollector {
            onStreamFinished: {
                try {
                    const data = JSON.parse(text);
                    if (data.current_weather) {
                        weatherTemp = data.current_weather.temperature;
                        weatherTempStr = weatherTemp.toFixed(1) + "°C";
                    }
                    weatherFetching = false;
                } catch (e) {
                    weatherTempStr = "--°C";
                    weatherFetching = false;
                }
            }
        }
    }

    Process {
        id: zigstatProcess
        running: true
        command: [Quickshell.shellDir + "/Programs/zigstat", updateInterval]
        stdout: SplitParser {
            onRead: function (line) {
                try {
                    const data = JSON.parse(line);
                    cpuUsage = +data.cpu;
                    // cpuTemp is now handled by sys_temps.py for better accuracy
                    memoryUsage = +data.mem;
                    memoryUsagePer = +data.memper;
                    diskUsage = +data.diskper;
                    cpuUsageStr = data.cpu + "%";
                    memoryUsageStr = data.mem + "G";
                    memoryUsagePerStr = data.memper + "%";
                    diskUsageStr = data.diskper + "%";
                } catch (e) {
                    console.error("Failed to parse zigstat output:", e);
                }
            }
        }
    }

    Timer {
        id: gpuUpdateTimer
        interval: 5000
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: gpuProcess.running = true
    }

    Process {
        id: gpuProcess
        command: ["cat", "/sys/class/drm/card1/device/mem_info_vram_used", "/sys/class/drm/card1/device/mem_info_vram_total"]
        stdout: StdioCollector {
            onStreamFinished: {
                const lines = text.trim().split("\n");
                if (lines.length >= 2) {
                    gpuMemUsed = parseInt(lines[0]);
                    gpuMemUsageStr = (gpuMemUsed / (1024 * 1024 * 1024)).toFixed(1) + "G";
                }
            }
        }
    }
}
