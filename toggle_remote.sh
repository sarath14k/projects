#!/bin/bash
STATUS=$(systemctl --user is-active webremote)
echo "$(date): Current status is $STATUS" >> /tmp/toggle.log
if [[ "$STATUS" == "active" ]]; then
    echo "Stopping..." >> /tmp/toggle.log
    systemctl --user stop webremote
else
    echo "Starting..." >> /tmp/toggle.log
    # Just try to start; systemd handles conflicts usually
    # But we'll do a quick cleanup just in case
    fuser -k 5000/tcp 2>/dev/null
    systemctl --user start webremote
fi
echo "$(date): New status is $(systemctl --user is-active webremote)" >> /tmp/toggle.log
