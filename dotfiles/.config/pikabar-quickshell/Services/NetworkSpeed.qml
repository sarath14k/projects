pragma Singleton
import QtQuick
import Quickshell
import Quickshell.Io

Singleton {
    id: root
    property real downloadSpeed: 0
    property real uploadSpeed: 0
    property string downloadSpeedStr: "0 B/s"
    property string uploadSpeedStr: "0 B/s"

    property var lastBytes: ({rx: 0, tx: 0, time: 0})

    function formatSpeed(bytes) {
        if (bytes < 1024) return bytes.toFixed(0) + " B/s";
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB/s";
        return (bytes / (1024 * 1024)).toFixed(1) + " MB/s";
    }

    Timer {
        interval: 2000
        // Only run when we have some network activity expected
        running: Network.anyConnected
        repeat: true
        onTriggered: {
            process.running = true;
        }
    }

    Process {
        id: process
        command: ["cat", "/proc/net/dev"]
        stdout: StdioCollector {
            onStreamFinished: {
                const lines = text.split("\n");
                let totalRx = 0;
                let totalTx = 0;
                for (let line of lines) {
                    if (line.includes(":")) {
                        const parts = line.trim().split(/\s+/);
                        totalRx += parseInt(parts[1]) || 0;
                        totalTx += parseInt(parts[9]) || 0;
                    }
                }
                const now = Date.now();
                if (lastBytes.time > 0) {
                    const dt = (now - lastBytes.time) / 1000;
                    if (dt > 0) {
                        downloadSpeed = (totalRx - lastBytes.rx) / dt;
                        uploadSpeed = (totalTx - lastBytes.tx) / dt;
                        downloadSpeedStr = formatSpeed(downloadSpeed);
                        uploadSpeedStr = formatSpeed(uploadSpeed);
                    }
                }
                lastBytes = {rx: totalRx, tx: totalTx, time: now};
            }
        }
    }
}
