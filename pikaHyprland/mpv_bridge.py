import http.server
import socketserver
import subprocess
import os
import sys
import argparse
import time
import json
from threading import Thread

# Configuration
PORT = 9999

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

class StreamHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Private-Network')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204); self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.send_response(200); self.send_header('Content-type', 'text/html'); self.end_headers()
            try:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                with open(os.path.join(base_dir, 'index.html'), 'rb') as f: self.wfile.write(f.read())
            except: self.wfile.write(b"MeetShare Active")
        elif self.path == '/api/link_audio':
            self.handle_api(self.link_audio_ports)
        elif self.path == '/api/launch_mpv':
            self.handle_api(self.launch_mpv_logic)
        else:
            self.send_response(404); self.end_headers()

    def handle_api(self, logic_func):
        try:
            result = logic_func()
            self.send_response(200); self.send_header('Content-type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            self.send_response(500); self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())

    def link_audio_ports(self):
        links = 0
        try:
            out_ports = subprocess.check_output(['pw-link', '-o']).decode().splitlines()
            in_ports = subprocess.check_output(['pw-link', '-i']).decode().splitlines()
            
            # Identify source ports
            mpv_out = [p for p in out_ports if 'mpv' in p.lower()]
            webcam_out = [p for p in out_ports if 'webcam' in p.lower() or 'c270' in p.lower()]
            chrome_out = [p for p in out_ports if any(x in p.lower() for x in ['chrome', 'chromium', 'brave', 'firefox'])]
            
            # Identify listener ports
            chrome_in = [p for p in in_ports if any(x in p.lower() for x in ['chrome', 'chromium', 'brave', 'firefox'])]
            
            # --- SMART HEADSET/SPEAKER DETECTION ---
            # 1. Try Bluetooth/Headset first
            headset_in = [p for p in in_ports if any(x in p.lower() for x in ['boult', 'airbass', 'bluez'])]
            
            # 2. Fallback to default system speakers if no headset is found
            if not headset_in:
                print("⚠️ Headset not found, falling back to system speakers...", flush=True)
                # Look for the default playback device (usually contains 'playback' or 'hdmi' or 'analog')
                headset_in = [p for p in in_ports if 'playback' in p.lower() and not any(x in p.lower() for x in ['chrome', 'chromium', 'brave', 'firefox'])]
            
            # --- THE CLEAN MIX ---
            
            # 1. UNLINK EVERYTHING FIRST (Fresh start for MPV)
            for m in mpv_out:
                try:
                    current_links = subprocess.check_output(['pw-link', '-l', m], stderr=subprocess.DEVNULL).decode().splitlines()
                    for line in current_links:
                        if '|->' in line:
                            target = line.split('|->')[1].strip()
                            subprocess.run(['pw-link', '-d', m, target])
                except: pass

            # 2. LINK ONLY TO DESIRED TARGETS
            
            # MPV -> Chrome (Meeting hears video)
            for m in mpv_out:
                for c in chrome_in:
                    subprocess.run(['pw-link', m, c])
                    links += 1
            
            # Webcam -> Chrome (Meeting hears you)
            for w in webcam_out:
                for c in chrome_in:
                    subprocess.run(['pw-link', w, c])
            
            # MPV -> Headset or Speakers (You hear video)
            for m in mpv_out:
                for h in headset_in:
                    subprocess.run(['pw-link', m, h])
                    links += 1
            
            # Chrome -> Headset or Speakers (You hear her)
            for c_o in chrome_out:
                for h in headset_in:
                    subprocess.run(['pw-link', c_o, h])
                    links += 1
                    
        except Exception as e:
            print(f"Error: {e}")
            
        return {"status": "success", "links": links}

    def launch_mpv_logic(self):
        file = subprocess.check_output(['zenity', '--file-selection']).decode().strip()
        subprocess.Popen(['mpv', '--title=MeetShare_MPV', '--ao=pipewire', file])
        time.sleep(2.0)
        self.link_audio_ports()
        return {"status": "success", "file": os.path.basename(file)}

if __name__ == "__main__":
    with ThreadedHTTPServer(("0.0.0.0", PORT), StreamHandler) as httpd:
        httpd.serve_forever()
