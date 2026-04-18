#!/bin/bash
# Subtitle Selector Engine for MeetShare Pro

VIDEO_PATH="$1"
LANG="en"
SUBLIMINAL="$HOME/.local/bin/subliminal"
DIR=$(dirname "$VIDEO_PATH")
FILE=$(basename "$VIDEO_PATH")

# 1. Get the list of available subtitles
# We'll use 'guessit' (part of subliminal) to make sure we search correctly
notify-send -t 2000 "🔍 Searching..." "Finding English subtitles for $FILE"

# For simplicity in this "Basic" version, we'll just download the best match 
# since subliminal's 'list' mode is harder to parse for a GUI.
# BUT we'll make it show a progress box so you know it's working.

(
echo "10" ; sleep 1
echo "# Connecting to OpenSubtitles..." ; sleep 1
$SUBLIMINAL download -l "$LANG" -d "$DIR" "$VIDEO_PATH" > /tmp/sub_res.log 2>&1
echo "100" ; sleep 1
) | zenity --progress --title="Subtitle Downloader" --text="Downloading best match..." --auto-close --no-cancel

if grep -q "Downloaded 1 subtitle" /tmp/sub_res.log; then
    notify-send "✅ Success" "Subtitles downloaded for $FILE"
    echo "SUCCESS"
else
    zenity --error --text="No subtitles found for this version of the movie."
    echo "FAIL"
fi
