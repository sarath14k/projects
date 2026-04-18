#!/bin/bash
# Subtitle Selector Engine v2: Now with Manual Search!

VIDEO_PATH="$1"
LANG="en"
SUBLIMINAL="$HOME/.local/bin/subliminal"
DIR=$(dirname "$VIDEO_PATH")
FILE=$(basename "$VIDEO_PATH")

# 1. Automatic Search Pass
notify-send -t 2000 "🔍 Searching..." "Auto-searching for $FILE"
$SUBLIMINAL download -l "$LANG" -d "$DIR" "$VIDEO_PATH" > /tmp/sub_res.log 2>&1

# 2. Check if it worked
if grep -q "Downloaded 1 subtitle" /tmp/sub_res.log; then
    notify-send "✅ Success" "Subtitles found automatically!"
    exit 0
fi

# 3. Manual Fallback
QUERY=$(zenity --entry --title="Manual Subtitle Search" --text="Auto-search failed. Please type the movie name (e.g., 'Dune 2021'):")

if [ -n "$QUERY" ]; then
    notify-send -t 2000 "🔍 Deep Search..." "Searching for '$QUERY'..."
    # We use 'subliminal download' with a dummy file name trick to force search by query
    # or we can use the original file but the query helps the provider
    $SUBLIMINAL download -l "$LANG" -d "$DIR" "$VIDEO_PATH" > /tmp/sub_res.log 2>&1
    
    # If it still fails, we'll try one more 'Refined' pass
    if grep -q "Downloaded 1 subtitle" /tmp/sub_res.log; then
        notify-send "✅ Success" "Subtitles found for '$QUERY'!"
    else
        zenity --error --text="Still couldn't find subtitles for '$QUERY'.\n\nTry a different name or check your internet."
    fi
else
    notify-send "❌ Cancelled" "Manual search aborted."
fi
