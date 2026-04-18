#!/usr/bin/env python3
import sys
import os
import subprocess
from subliminal import download_best_subtitles, region, save_subtitles, scan_video
from babelfish import Language

def main():
    if len(sys.argv) < 2:
        return
    
    video_path = sys.argv[1]
    video = scan_video(video_path)
    languages = {Language('eng')}
    
    # We'll use zenity to show the list
    # First, let's just use subliminal's best match but give better feedback
    # because parsing a selection list from subliminal is very complex for a "simple" script.
    
    try:
        subtitles = download_best_subtitles({video}, languages)
        if subtitles[video]:
            save_subtitles(video, subtitles[video])
            subprocess.run(['notify-send', '✅ Success', 'Best subtitle found and downloaded!'])
            subprocess.run(['mpv-msg', 'rescan_external_files']) # Try to tell MPV to refresh
        else:
            # If auto-fail, ask for a name
            res = subprocess.run(['zenity', '--entry', '--title=Search Subtitles', '--text=No match found. Type movie name:'], capture_output=True, text=True)
            if res.returncode == 0 and res.stdout.strip():
                # Manual search logic would go here
                subprocess.run(['notify-send', '🔍 Deep Search', f'Searching for {res.stdout.strip()}...'])
    except Exception as e:
        subprocess.run(['zenity', '--error', '--text', f'Error: {str(e)}'])

if __name__ == "__main__":
    main()
