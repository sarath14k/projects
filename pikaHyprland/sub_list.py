#!/usr/bin/env python3
import sys
import os
import subprocess
from subliminal import list_subtitles, scan_video, save_subtitles, download_subtitles
from babelfish import Language

def get_label(sub):
    for attr in ['release_info', 'filename', 'title']:
        val = getattr(sub, attr, None)
        if val: return str(val)
    return str(sub)

def main():
    if len(sys.argv) < 2: return
    video_path = sys.argv[1]
    video_dir = os.path.dirname(os.path.abspath(video_path))
    
    try:
        video = scan_video(video_path)
        languages = {Language('eng')}
        
        subs = list_subtitles({video}, languages)
        found_subs = subs[video]
        
        if not found_subs:
            subprocess.run(['zenity', '--info', '--text', 'No approximate subtitles found.'])
            return

        zenity_args = ['zenity', '--list', '--title=Pick a Subtitle', '--column=ID', '--column=Provider', '--column=Release Version', '--width=800', '--height=500']
        for i, sub in enumerate(found_subs):
            zenity_args.append(str(i))
            zenity_args.append(getattr(sub, 'provider_name', 'Unknown'))
            zenity_args.append(get_label(sub))
            
        res = subprocess.run(zenity_args, capture_output=True, text=True)
        
        if res.returncode == 0:
            choice_index = int(res.stdout.strip())
            chosen_sub = found_subs[choice_index]
            
            subprocess.run(['notify-send', '📥 Downloading...', get_label(chosen_sub)])
            
            # DOWNLOAD & FORCE SAVE TO VIDEO DIRECTORY
            download_subtitles([chosen_sub])
            save_subtitles(video, [chosen_sub], directory=video_dir)
            
            subprocess.run(['notify-send', '✅ Success', f'Subtitles saved to: {video_dir}'])
            
    except Exception as e:
        subprocess.run(['zenity', '--error', '--text', f'Error: {str(e)}'])

if __name__ == "__main__":
    main()
