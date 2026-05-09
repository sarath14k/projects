#!/bin/bash
W_DIR="/home/sarath/wallpapers"
for f in "$W_DIR"/*.3840x2160.mp4; do
    base=$(basename "$f" .3840x2160.mp4)
    out="$W_DIR/$base.1080p.mp4"
    if [ ! -f "$out" ]; then
        ffmpeg -i "$f" -vf scale=1920:1080 -c:v libx264 -preset fast -crf 20 -an "$out" -y
    fi
done
