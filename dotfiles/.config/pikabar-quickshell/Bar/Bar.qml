import QtQuick
import QtQuick.Controls
import QtQuick.Effects
import QtQuick.Layouts
import Quickshell
import Quickshell.Io
import Quickshell.Wayland
import qs.Bar.Modules
import qs.Components
import qs.Helpers
import qs.Services
import qs.Settings
import qs.Widgets
import qs.Widgets.Notification
import qs.Widgets.SidePanel

// Main bar component - creates panels on selected monitors with widgets and corners
Scope {
    id: rootScope

    property var shell
    property alias visible: barRootItem.visible

    Item {
        id: barRootItem

        anchors.fill: parent

        Variants {
            model: Quickshell.screens

            Item {
                property var modelData

                PanelWindow {
                    id: panel

                    property bool isShrunk: false

                    screen: modelData
                    color: "transparent"
                    implicitHeight: (panel.isShrunk ? 40 : 44) * Theme.scale(panel.screen)
                    anchors.top: true
                    anchors.left: true
                    anchors.right: true
                    WlrLayershell.namespace: "pikabar"
                    WlrLayershell.exclusionMode: ExclusionMode.Exclusive
                    visible: Settings.settings.barMonitors.includes(modelData.name) || (Settings.settings.barMonitors.length === 0)

                    Behavior on implicitHeight {
                        NumberAnimation { duration: 350; easing.type: Easing.OutCubic }
                    }

                    Item {
                        id: barContainer
                        anchors.fill: parent

                        states: [
                            State {
                                name: "shrunk"
                                when: panel.isShrunk
                                AnchorChanges {
                                    target: workspace
                                    anchors.horizontalCenter: undefined
                                    anchors.left: leftWidgetsRow.right
                                }
                                AnchorChanges {
                                    target: rightWidgetsRow
                                    anchors.right: undefined
                                    anchors.left: workspace.right
                                }
                                PropertyChanges {
                                    target: workspace
                                    anchors.leftMargin: 24 * Theme.scale(panel.screen)
                                }
                                PropertyChanges {
                                    target: rightWidgetsRow
                                    anchors.leftMargin: 24 * Theme.scale(panel.screen)
                                }
                            }
                        ]

                        transitions: [
                            Transition {
                                from: "*"
                                to: "*"
                                AnchorAnimation {
                                    duration: 350
                                    easing.type: Easing.OutCubic
                                }
                            }
                        ]

                        Rectangle {
                            id: barBackground

                        width: panel.isShrunk
                            ? (leftWidgetsRow.width + workspace.width + rightWidgetsRow.width + 84 * Theme.scale(panel.screen))
                            : (parent.width - 32 * Theme.scale(panel.screen))
                        height: (panel.isShrunk ? 34 : 38) * Theme.scale(panel.screen)
                        color: Qt.rgba(Theme.surface.r, Theme.surface.g, Theme.surface.b, 0.45)
                        radius: 12 * Theme.scale(panel.screen)
                        anchors.top: parent.top
                        anchors.topMargin: (panel.isShrunk ? 5 : 6) * Theme.scale(panel.screen)
                        anchors.horizontalCenter: parent.horizontalCenter
                        
                        border.width: 1
                        border.color: panel.isShrunk 
                            ? Qt.rgba(0.05, 0.72, 0.83, 0.35) 
                            : Qt.rgba(255, 255, 255, 0.08)

                        Behavior on border.color {
                            ColorAnimation { duration: 350 }
                        }

                        layer.enabled: true
                        layer.effect: MultiEffect {
                            blurEnabled: true
                            blur: 1.0 // Maximized Frosted Look
                            shadowEnabled: true
                            shadowColor: "#60000000"
                            shadowBlur: 0.5
                            shadowVerticalOffset: 2 * Theme.scale(panel.screen)
                        }

                        Behavior on width {
                            NumberAnimation { duration: 350; easing.type: Easing.OutCubic }
                        }
                        Behavior on height {
                            NumberAnimation { duration: 350; easing.type: Easing.OutCubic }
                        }
                        Behavior on anchors.topMargin {
                            NumberAnimation { duration: 350; easing.type: Easing.OutCubic }
                        }

                        MouseArea {
                            anchors.fill: parent
                            propagateComposedEvents: true
                            cursorShape: Qt.PointingHandCursor
                            onDoubleClicked: (mouse) => {
                                panel.isShrunk = !panel.isShrunk;
                                mouse.accepted = false;
                            }
                        }
                    }

                    Item {
                        id: barContent
                        anchors.fill: barBackground

                        Row {
                            id: leftWidgetsRow

                            anchors.verticalCenter: parent.verticalCenter
                            anchors.left: parent.left
                            anchors.leftMargin: 18 * Theme.scale(panel.screen)
                            spacing: 12 * Theme.scale(panel.screen)
                            
                            scale: panel.isShrunk ? 0.92 : 1.0
                            transformOrigin: Item.Left

                            Behavior on scale {
                                NumberAnimation { duration: 350; easing.type: Easing.OutCubic }
                            }
                            Behavior on spacing {
                                NumberAnimation { duration: 350; easing.type: Easing.OutCubic }
                            }

                            SystemInfo {
                                anchors.verticalCenter: parent.verticalCenter
                            }


                            Taskbar {
                                screen: modelData
                                anchors.verticalCenter: parent.verticalCenter
                            }

                        }

                        ActiveWindow {
                            screen: modelData
                        }

                        Workspace {
                            id: workspace

                            screen: modelData
                            anchors.horizontalCenter: parent.horizontalCenter
                            anchors.verticalCenter: parent.verticalCenter

                            scale: panel.isShrunk ? 0.92 : 1.0
                            transformOrigin: Item.Center

                            Behavior on scale {
                                NumberAnimation { duration: 350; easing.type: Easing.OutCubic }
                            }
                        }

                        Row {
                            id: rightWidgetsRow

                            anchors.verticalCenter: parent.verticalCenter
                            anchors.right: parent.right
                            anchors.rightMargin: 18 * Theme.scale(panel.screen)
                            spacing: 10 * Theme.scale(panel.screen)
                        
                        scale: panel.isShrunk ? 0.92 : 1.0
                        transformOrigin: Item.Right

                        Behavior on scale {
                            NumberAnimation { duration: 350; easing.type: Easing.OutCubic }
                        }
                        Behavior on spacing {
                            NumberAnimation { duration: 350; easing.type: Easing.OutCubic }
                        }

                        CustomTrayMenu {
                            id: externalTrayMenu
                        }

                        PanelPopup {
                            id: sidebarPopup
                            shell: rootScope.shell
                        }

                        // 1. System Tray Pill
                        Rectangle {
                            id: trayPill
                            height: 28 * Theme.scale(panel.screen)
                            width: trayRow.implicitWidth + 16 * Theme.scale(panel.screen)
                            radius: 8 * Theme.scale(panel.screen)
                            color: Qt.rgba(Theme.surfaceVariant.r, Theme.surfaceVariant.g, Theme.surfaceVariant.b, 0.35)
                            border.width: 1
                            border.color: Qt.rgba(255, 255, 255, 0.06)
                            anchors.verticalCenter: parent.verticalCenter

                            Row {
                                id: trayRow
                                height: parent.height
                                anchors.centerIn: parent
                                spacing: 8 * Theme.scale(panel.screen)

                                SystemTray {
                                    id: systemTrayModule
                                    shell: rootScope.shell
                                    anchors.verticalCenter: parent.verticalCenter
                                    bar: panel
                                    trayMenu: externalTrayMenu
                                }

                                UpdateManager {
                                    shell: rootScope.shell
                                    anchors.verticalCenter: parent.verticalCenter
                                }

                                NotificationIcon {
                                    shell: rootScope.shell
                                    anchors.verticalCenter: parent.verticalCenter
                                }
                            }
                        }

                        // 2. Network / Connectivity Pill
                        Rectangle {
                            id: networkPill
                            height: 28 * Theme.scale(panel.screen)
                            width: networkRow.implicitWidth + 16 * Theme.scale(panel.screen)
                            radius: 8 * Theme.scale(panel.screen)
                            color: Qt.rgba(Theme.surfaceVariant.r, Theme.surfaceVariant.g, Theme.surfaceVariant.b, 0.35)
                            border.width: 1
                            border.color: Qt.rgba(255, 255, 255, 0.06)
                            anchors.verticalCenter: parent.verticalCenter

                            Row {
                                id: networkRow
                                height: parent.height
                                anchors.centerIn: parent
                                spacing: 8 * Theme.scale(panel.screen)

                                NetworkIndicator {
                                    anchors.verticalCenter: parent.verticalCenter
                                }

                                Ethernet {
                                    anchors.verticalCenter: parent.verticalCenter
                                }

                                Wifi {
                                    anchors.verticalCenter: parent.verticalCenter
                                }

                                Bluetooth {
                                    anchors.verticalCenter: parent.verticalCenter
                                }

                                WebRemote {
                                    screen: panel.screen
                                    anchors.verticalCenter: parent.verticalCenter
                                }
                            }
                        }

                        // 3. System Controls Pill
                        Rectangle {
                            id: controlsPill
                            height: 28 * Theme.scale(panel.screen)
                            width: controlsRow.implicitWidth + 16 * Theme.scale(panel.screen)
                            radius: 8 * Theme.scale(panel.screen)
                            color: Qt.rgba(Theme.surfaceVariant.r, Theme.surfaceVariant.g, Theme.surfaceVariant.b, 0.35)
                            border.width: 1
                            border.color: Qt.rgba(255, 255, 255, 0.06)
                            anchors.verticalCenter: parent.verticalCenter

                            Row {
                                id: controlsRow
                                height: parent.height
                                anchors.centerIn: parent
                                spacing: 8 * Theme.scale(panel.screen)

                                PowerMode {
                                    anchors.verticalCenter: parent.verticalCenter
                                }
                                
                                Battery {
                                    id: widgetsBattery
                                    anchors.verticalCenter: parent.verticalCenter
                                }

                                Brightness {
                                    id: widgetsBrightness
                                    screen: modelData
                                    anchors.verticalCenter: parent.verticalCenter
                                }

                                Volume {
                                    id: widgetsVolume
                                    shell: rootScope.shell
                                    anchors.verticalCenter: parent.verticalCenter
                                }
                            }
                        }

                        // 4. Clock Pill
                        Rectangle {
                            id: clockPill
                            height: 28 * Theme.scale(panel.screen)
                            width: clockRow.implicitWidth + 16 * Theme.scale(panel.screen)
                            radius: 8 * Theme.scale(panel.screen)
                            color: Qt.rgba(Theme.surfaceVariant.r, Theme.surfaceVariant.g, Theme.surfaceVariant.b, 0.35)
                            border.width: 1
                            border.color: Qt.rgba(255, 255, 255, 0.06)
                            anchors.verticalCenter: parent.verticalCenter

                            Row {
                                id: clockRow
                                height: parent.height
                                anchors.centerIn: parent
                                spacing: 6 * Theme.scale(panel.screen)

                                Text {
                                    font.family: "Material Symbols Outlined"
                                    font.pixelSize: Theme.fontSizeSmall * Theme.scale(panel.screen)
                                    text: "schedule"
                                    color: "#FFD600" // Vibrant neon gold
                                    verticalAlignment: Text.AlignVCenter
                                    anchors.verticalCenter: parent.verticalCenter
                                }

                                ClockWidget {
                                    screen: modelData
                                    anchors.verticalCenter: parent.verticalCenter
                                }
                            }
                        }

                        Button {
                            barBackground: barBackground
                            anchors.verticalCenter: parent.verticalCenter
                            screen: modelData
                            sidebarPopup: sidebarPopup
                        }

                    }

                    } // closes barContent

                }

            }

                Loader {
                    active: Settings.settings.showCorners && (Settings.settings.barMonitors.includes(modelData.name) || (Settings.settings.barMonitors.length === 0))

                    sourceComponent: Item {
                        PanelWindow {
                            id: topLeftPanel

                            anchors.top: true
                            anchors.left: true
                            color: "transparent"
                            screen: modelData
                            margins.top: 44 * Theme.scale(screen) - 1
                            WlrLayershell.exclusionMode: ExclusionMode.Ignore
                            WlrLayershell.layer: WlrLayer.Top
                            WlrLayershell.namespace: "pikabar"
                            aboveWindows: false
                            implicitHeight: 24

                            Corner {
                                id: topLeftCorner

                                position: "bottomleft"
                                size: 1.3
                                fillColor: barBackground.color
                                offsetX: -39
                                offsetY: 0
                                anchors.top: parent.top
                            }

                        }

                        PanelWindow {
                            id: topRightPanel

                            anchors.top: true
                            anchors.right: true
                            color: "transparent"
                            screen: modelData
                            margins.top: 44 * Theme.scale(screen) - 1
                            WlrLayershell.exclusionMode: ExclusionMode.Ignore
                            WlrLayershell.layer: WlrLayer.Top
                            WlrLayershell.namespace: "pikabar"
                            aboveWindows: false
                            implicitHeight: 24

                            Corner {
                                id: topRightCorner

                                position: "bottomright"
                                size: 1.3
                                fillColor: barBackground.color
                                offsetX: 39
                                offsetY: 0
                                anchors.top: parent.top
                            }

                        }

                        PanelWindow {
                            id: bottomLeftPanel

                            anchors.bottom: true
                            anchors.left: true
                            color: "transparent"
                            screen: modelData
                            WlrLayershell.exclusionMode: ExclusionMode.Ignore
                            WlrLayershell.layer: WlrLayer.Top
                            WlrLayershell.namespace: "swww-daemon"
                            aboveWindows: false
                            implicitHeight: 24

                            Corner {
                                id: bottomLeftCorner

                                position: "topleft"
                                size: 1.3
                                fillColor: barBackground.color
                                offsetX: -39
                                offsetY: 0
                                anchors.top: parent.top
                            }

                        }

                        PanelWindow {
                            id: bottomRightPanel

                            anchors.bottom: true
                            anchors.right: true
                            color: "transparent"
                            screen: modelData
                            WlrLayershell.exclusionMode: ExclusionMode.Ignore
                            WlrLayershell.layer: WlrLayer.Top
                            WlrLayershell.namespace: "swww-daemon"
                            aboveWindows: false
                            implicitHeight: 24

                            Corner {
                                id: bottomRightCorner

                                position: "topright"
                                size: 1.3
                                fillColor: barBackground.color
                                offsetX: 39
                                offsetY: 0
                                anchors.top: parent.top
                            }

                        }

                    }

                }

            }

        }

    }

}
