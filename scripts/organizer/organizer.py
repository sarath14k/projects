#!/usr/bin/env python3
import os
import shutil
import time
import re
from pathlib import Path

# Paths
DOWNLOADS_DIR = Path.home() / "Downloads"
CONFIG = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".tex"],
    "Spreadsheets": [".csv", ".xls", ".xlsx", ".ods"],
    "Presentations": [".pptx", ".ppt", ".odp"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Video": [".mp4", ".mkv", ".flv", ".avi", ".mov", ".wmv"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar", ".bz2"],
    "Executables": [".exe", ".msi", ".deb", ".rpm", ".sh", ".bin"],
    "ISOs": [".iso", ".img"],
    "Torrent": [".torrent"]
}

# Regex for detecting series (e.g. S01E01, 1x01, Season 1, etc.)
SERIES_PATTERN = re.compile(r"([sS]\d+[eE]\d+)|(\d+x\d+)|([sS]eason\s*\d+)|([eE]pisode\s*\d+)", re.IGNORECASE)
# Regex for detecting movies (e.g. Movie (2023), Movie 2023)
MOVIE_PATTERN = re.compile(r"\(?\d{4}\)?")

# Settings to prevent moving active downloads
TEMP_EXTENSIONS = [".!qb", ".part", ".crdownload", ".tmp", ".download"]
SETTLE_DOWN_TIME = 60 # seconds

def move_item(item, folder_name):
    """Moves an item to the specified folder within DOWNLOADS_DIR, handling collisions."""
    dest_dir = DOWNLOADS_DIR / folder_name
    dest_dir.mkdir(exist_ok=True)
    
    dest_path = dest_dir / item.name
    
    if dest_path.exists():
        if item.is_file():
            base = item.stem
            ext = item.suffix
            counter = 1
            while (dest_dir / f"{base}_{counter}{ext}").exists():
                counter += 1
            dest_path = dest_dir / f"{base}_{counter}{ext}"
        else:
            base = item.name
            counter = 1
            while (dest_dir / f"{base}_{counter}").exists():
                counter += 1
            dest_path = dest_dir / f"{base}_{counter}"
            
    try:
        shutil.move(str(item), str(dest_path))
        print(f"Moved: {item.name} -> {folder_name}/")
        return True
    except Exception as e:
        print(f"Error moving {item.name} to {folder_name}: {e}")
        return False

def organize_dir(target_dir):
    """Scans and organizes a specific directory."""
    if not target_dir.exists():
        return

    now = time.time()
    # Folders that should NEVER be moved
    PROTECTED_FOLDERS = {
        "Desktop", "Documents", "Downloads", "Music", "Pictures", 
        "Public", "Templates", "Videos", "DeviceDetectionSysInfo", 
        "projects", "wallpapers", "dotfiles", "Telegram Desktop"
    } | set(CONFIG.keys()) | {"Movies", "Series", "ISOs", "Others"}

    for item in target_dir.iterdir():
        # Skip hidden files
        if item.name.startswith("."):
            continue
            
        # Skip protected folders
        if item.is_dir() and item.name in PROTECTED_FOLDERS:
            continue
            
        # Settle-down period: skip items that were modified very recently
        try:
            mtime = item.stat().st_mtime
            if now - mtime < SETTLE_DOWN_TIME:
                continue
        except FileNotFoundError:
            continue

        if item.is_file():
            extension = item.suffix.lower()
            if extension in TEMP_EXTENSIONS:
                continue

            # Handle Videos
            if extension in CONFIG["Video"]:
                if SERIES_PATTERN.search(item.name):
                    move_item(item, "Series")
                else:
                    move_item(item, "Movies")
                continue

            # Handle other files based on CONFIG
            moved = False
            for folder, extensions in CONFIG.items():
                if extension in extensions:
                    move_item(item, folder)
                    moved = True
                    break
            
            if not moved:
                # For Home directory, don't move unknown files to "Others" automatically
                # to avoid cluttering or moving system scripts incorrectly.
                # Only move to Others if we are in Downloads.
                if target_dir == DOWNLOADS_DIR:
                    move_item(item, "Others")

        elif item.is_dir():
            # Handle directory organization (primarily for media)
            if SERIES_PATTERN.search(item.name):
                move_item(item, "Series")
            elif MOVIE_PATTERN.search(item.name):
                move_item(item, "Movies")

def organize():
    # Organize both Home and Downloads
    organize_dir(DOWNLOADS_DIR)
    organize_dir(Path.home())

if __name__ == "__main__":
    organize()
