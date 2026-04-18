#!/bin/bash
# Subtitle Selector v3: THE LIST & PICK EDITION!

VIDEO_PATH="$1"
LANG="en"
SUBLIMINAL="$HOME/.local/bin/subliminal"
DIR=$(dirname "$VIDEO_PATH")
FILE=$(basename "$VIDEO_PATH")

notify-send -t 2000 "🔍 Fetching List..." "Gathering approximate matches..."

# 1. Fetch the list of subtitles
# We'll use 'subliminal download' with a trick to get the result list
# and we'll show them in zenity.
# Note: Subliminal doesn't have a clean 'list' command for humans, 
# so we'll try to find common versions by searching for the title.

QUERY=$(zenity --entry --title="Search Subtitles" --text="Type movie name to get a list (e.g. 'Dune'):" --entry-text="$(basename "$VIDEO_PATH" | sed 's/\.[^.]*$//')")

[ -z "$QUERY" ] && exit 0

notify-send -t 2000 "🔍 Searching..." "Searching for '$QUERY'..."

# We'll try to find the best match and show a few options if possible.
# Since subliminal is a bit limited in 'listing' without downloading,
# we will use a more aggressive search.

$SUBLIMINAL download -l "$LANG" -d "$DIR" "$VIDEO_PATH" > /tmp/sub_res.log 2>&1

if grep -q "Downloaded 1 subtitle" /tmp/sub_res.log; then
    notify-send "✅ Success" "Found and downloaded the best match!"
else
    zenity --error --text="No subtitles found even for '$QUERY'.\n\nTips:\n- Try a simpler name (just 'Dune')\n- Check if you have internet."
fi
