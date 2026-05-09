pragma Singleton
import QtQuick
import Quickshell
import "../Helpers/Holidays.js" as HolidayHelper

Singleton {
    id: root

    property string todayHoliday: ""
    property date lastChecked: new Date(0)

    function checkHolidays() {
        const now = new Date();
        // Only check once per day
        if (now.getDate() === lastChecked.getDate() && 
            now.getMonth() === lastChecked.getMonth() && 
            now.getFullYear() === lastChecked.getFullYear()) {
            return;
        }

        HolidayHelper.getHolidaysForMonth(now.getFullYear(), now.getMonth(), function(holidays) {
            const todayStr = Qt.formatDate(now, "yyyy-MM-dd");
            const holiday = holidays.find(h => h.date === todayStr);
            todayHoliday = holiday ? "🎉 " + holiday.name : "";
            lastChecked = now;
        });
    }

    // Refresh every hour just in case
    Timer {
        interval: 3600000
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: root.checkHolidays()
    }
}
