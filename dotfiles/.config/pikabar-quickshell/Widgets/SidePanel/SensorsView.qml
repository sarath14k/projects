import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import qs.Components
import qs.Services
import qs.Settings

Item {
    id: root
    implicitWidth: 420 * Theme.scale(Screen)
    
    property bool show: false
    height: show ? sensorsContent.height : 0
    opacity: show ? 1 : 0
    visible: opacity > 0
    clip: true

    Behavior on height {
        NumberAnimation { duration: 400; easing.type: Easing.OutCubic }
    }
    
    Behavior on opacity {
        NumberAnimation { duration: 300 }
    }

    property var sensorsData: Sysinfo.allSensors

    ColumnLayout {
        id: sensorsContent
        width: parent.width
        spacing: 12 * Theme.scale(Screen)

        Repeater {
            model: Object.keys(root.sensorsData)

            delegate: Rectangle {
                id: deviceCard
                Layout.fillWidth: true
                height: deviceLayout.implicitHeight + (24 * Theme.scale(Screen))
                radius: 12 * Theme.scale(Screen)
                color: Theme.surface
                border.color: Theme.outlineVariant
                border.width: 1

                ColumnLayout {
                    id: deviceLayout
                    anchors.fill: parent
                    anchors.margins: 12 * Theme.scale(Screen)
                    spacing: 8 * Theme.scale(Screen)

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 8 * Theme.scale(Screen)

                        Text {
                            text: getIcon(modelData)
                            font.family: "Material Symbols Outlined"
                            font.pixelSize: 18 * Theme.scale(Screen)
                            color: Theme.accentPrimary
                        }

                        Text {
                            text: modelData
                            font.family: Theme.fontFamily
                            font.pixelSize: 14 * Theme.scale(Screen)
                            font.weight: Font.Bold
                            color: Theme.textPrimary
                            Layout.fillWidth: true
                        }
                    }

                    GridLayout {
                        columns: 2
                        Layout.fillWidth: true
                        rowSpacing: 4 * Theme.scale(Screen)
                        columnSpacing: 16 * Theme.scale(Screen)

                        Repeater {
                            model: root.sensorsData[modelData]

                            delegate: Item {
                                Layout.fillWidth: true
                                height: 24 * Theme.scale(Screen)

                                RowLayout {
                                    anchors.fill: parent
                                    spacing: 8 * Theme.scale(Screen)

                                    Text {
                                        text: modelData.label
                                        font.family: Theme.fontFamily
                                        font.pixelSize: 13 * Theme.scale(Screen)
                                        color: Theme.textSecondary
                                        Layout.fillWidth: true
                                    }

                                    Text {
                                        text: modelData.value.toFixed(1) + "°C"
                                        font.family: Theme.fontFamily
                                        font.pixelSize: 13 * Theme.scale(Screen)
                                        font.weight: Font.Medium
                                        color: getTempColor(modelData.value)
                                    }

                                    Text {
                                        text: modelData.status.split(' ')[0] // Emoji only
                                        font.pixelSize: 14 * Theme.scale(Screen)
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    function getIcon(name) {
        if (name.includes("CPU")) return "processor";
        if (name.includes("GPU")) return "videogame_asset";
        if (name.includes("NVMe") || name.includes("Storage")) return "storage";
        if (name.includes("Motherboard")) return "developer_board";
        if (name.includes("Network")) return "router";
        if (name.includes("ACPI")) return "thermostat";
        return "sensors";
    }

    function getTempColor(temp) {
        if (temp < 45) return "#4FC3F7"; // Cool Blue
        if (temp < 65) return "#81C784"; // Healthy Green
        if (temp < 80) return "#FFB74D"; // Warm Orange
        return "#E57373"; // Hot Red
    }
}
