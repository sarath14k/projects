#!/bin/bash

# Configuration
QUERY="cyberpunk"
RESOLUTION="2560x1440"
DEST="/home/sarath/wallpapers/live_wallpaper.png"
API_URL="https://wallhaven.cc/api/v1/search"

echo "Fetching new 2K wallpaper from Wallhaven..."

# Search for the top-rated 2K wallpaper
IMAGE_URL=$(curl -s "${API_URL}?q=${QUERY}&resolutions=${RESOLUTION}&sorting=toplist" | jq -r '.data[0].path')

if [ -z "$IMAGE_URL" ] || [ "$IMAGE_URL" == "null" ]; then
    echo "Failed to fetch image URL."
    exit 1
fi

echo "Downloading $IMAGE_URL..."
curl -L "$IMAGE_URL" -o "$DEST"

echo "Done! New wallpaper saved to $DEST"
