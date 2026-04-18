#!/usr/bin/env python3
import sys
import os
import subprocess
from subliminal import list_subtitles, scan_video, save_subtitles, download_subtitles
from babelfish import Language

def main():
    if len(sys.argv) < 2: return
    video_path = sys.argv[1]
    
    try:
        video = scan_video(video_path)
        languages = {Language('eng')}
        
        # 1. Fetch ALL approximate subtitles
        subs = list_subtitles({video}, languages)
        found_subs = subs[video]
        
        if not found_subs:
            subprocess.run(['zenity', '--info', '--text', 'No approximate subtitles found.'])
            return

        # 2. Format for Zenity List
        # Columns: Index | Provider | Release Name
        zenity_args = ['zenity', '--list', '--title=Pick a Subtitle', '--column=ID', '--column=Provider', '--column=Release Name', '--width=800', '--height=500']
        
        for i, sub in enumerate(found_subs):
            zenity_args.append(str(i))
            zenity_args.append(sub.provider_name)
            zenity_args.append(sub.release_info or "Unknown Release")
            
        res = subprocess.run(zenity_args, capture_output=True, text=True)
        
        if res.returncode == 0:
            choice_index = int(res.stdout.strip())
            chosen_sub = found_subs[choice_index]
            
            subprocess.run(['notify-send', '📥 Downloading...', chosen_sub.release_info])
            download_subtitles([chosen_sub])
            save_subtitles(video, [chosen_sub])
            subprocess.run(['notify-send', '✅ Success', 'Subtitles saved!'])
            
    except Exception as e:
        subprocess.run(['zenity', '--error', '--text', f'Error: {str(e)}'])

if __name__ == "__main__":
    main()
