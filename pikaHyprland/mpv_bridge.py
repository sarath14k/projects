import http.server
import socketserver
import subprocess
import os
import sys
import time
import json
import socket
from threading import Thread
from datetime import datetime

# Performance Constants
PORT = 9999
IPC_SOCKET = "/tmp/meetshare-mpv.sock"
MAX_LOGS = 25

# Global State
state = {
    "mic_active": True,
    "logs": [],
    "last_sync": 0
}

def add_log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {msg}"
    state["logs"].append(entry)
    if len(state["logs"]) > MAX_LOGS: state["logs"].pop(0)
    print(entry)

class FastAPIHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Private-Network')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204); self.end_headers()

    def serve_file(self, filename, content_type):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(base_dir, filename), 'rb') as f:
                self.send_response(200); self.send_header('Content-type', content_type); self.end_headers()
                self.wfile.write(f.read())
        except: self.send_error(404)

    def json_resp(self, data):
        self.send_response(200); self.send_header('Content-type', 'application/json'); self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        path = self.path
        if path == '/': self.serve_file('index.html', 'text/html')
        elif path == '/api/link_audio': self.json_resp(self.server.engine.sync())
        elif path == '/api/launch_mpv': self.json_resp(self.server.engine.launch())
        elif path == '/api/toggle_mic': self.json_resp(self.server.engine.toggle_mic())
        elif path == '/api/logs': self.json_resp({"logs": state["logs"]})
        elif path == '/api/get_volume': self.json_resp({"volume": self.server.engine.query_mpv("volume")})
        elif '/api/vol_' in path: self.json_resp(self.server.engine.change_volume(5 if 'up' in path else -5))
        elif '/api/set_volume' in path: self.json_resp(self.server.engine.set_volume(path.split('=')[-1]))
        else: super().do_GET()

class MeetEngine:
    def query_mpv(self, prop):
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.settimeout(0.1); s.connect(IPC_SOCKET)
                s.sendall(json.dumps({"command": ["get_property", prop]}).encode() + b'\n')
                return json.loads(s.recv(1024).decode()).get('data', 100)
        except: return 100

    def set_volume(self, vol):
        return self.send_mpv_cmd(["set_property", "volume", int(vol)], f"Volume: {vol}%")

    def change_volume(self, delta):
        return self.send_mpv_cmd(["add", "volume", delta], f"Volume adjusted")

    def send_mpv_cmd(self, cmd_list, log_msg):
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.connect(IPC_SOCKET)
                s.sendall(json.dumps({"command": cmd_list}).encode() + b'\n')
            add_log(log_msg); return {"status": "ok"}
        except: return {"status": "error"}

    def toggle_mic(self):
        state["mic_active"] = not state["mic_active"]
        add_log(f"Mic: {'ENABLED' if state['mic_active'] else 'MUTED'}")
        return self.sync()

    def sync(self):
        try:
            out_p = subprocess.check_output(['pw-link', '-o']).decode().splitlines()
            in_p = subprocess.check_output(['pw-link', '-i']).decode().splitlines()
            mpv_o = [p for p in out_p if 'mpv' in p.lower()]
            web_o = [p for p in out_p if any(x in p.lower() for x in ['webcam', 'c270'])]
            brw_o = [p for p in out_p if any(x in p.lower() for x in ['chrome', 'firefox', 'brave'])]
            brw_i = [p for p in in_p if any(x in p.lower() for x in ['chrome', 'firefox', 'brave'])]
            hds_i = [p for p in in_p if any(x in p.lower() for x in ['boult', 'bluez', 'airbass'])]
            
            # 1. FULL SECTOR PURGE: Scan every single source and KILL any link to HDMI
            for source in out_p:
                try:
                    # See where this specific source is sending its audio
                    current = subprocess.check_output(['pw-link', '-l', source], stderr=subprocess.DEVNULL).decode().splitlines()
                    for line in current:
                        if '|->' in line:
                            target = line.split('|->')[1].strip()
                            if 'hdmi' in target.lower():
                                # KILL the link to room speakers
                                subprocess.run(['pw-link', '-d', source, target])
                except: pass

            # 2. MOVIE CLEANUP: Unlink MPV from its old targets
            for m in mpv_o:
                try:
                    current = subprocess.check_output(['pw-link', '-l', m], stderr=subprocess.DEVNULL).decode().splitlines()
                    for line in current:
                        if '|->' in line:
                            target = line.split('|->')[1].strip()
                            subprocess.run(['pw-link', '-d', m, target])
                except: pass

            links = 0
            if state["mic_active"]:
                for w in web_o: 
                    for b in brw_i: subprocess.run(['pw-link', w, b]); links += 1
                    # MONITORING: Force her voice into the Headset ONLY
                    for h in hds_i:
                        if 'playback' in h.lower():
                            subprocess.run(['pw-link', w, h]); links += 1
            for m in mpv_o:
                for b in brw_i: subprocess.run(['pw-link', m, b]); links += 1
                for h in hds_i: 
                    if 'playback' in h.lower():
                        subprocess.run(['pw-link', m, h]); links += 1
            for b in brw_o:
                for h in hds_i: 
                    if 'playback' in h.lower():
                        subprocess.run(['pw-link', b, h]); links += 1

            add_log(f"Matrix Synced. Links: {links}")
            subprocess.run(['notify-send', '-t', '1500', 'MeetShare Pro', f'Matrix Synced ({links} links)'])
            return {"status": "success", "links": links, "mic_active": state["mic_active"]}
        except Exception as e:
            add_log(f"Sync Error: {str(e)}"); return {"status": "error"}

    def launch(self):
        try:
            file = subprocess.check_output(['zenity', '--file-selection']).decode().strip()
            if os.path.exists(IPC_SOCKET): os.remove(IPC_SOCKET)
            proc = subprocess.Popen(['mpv', f'--input-ipc-server={IPC_SOCKET}', '--title=MeetShare_MPV', '--ao=pipewire', '--sub-auto=fuzzy', file])
            add_log(f"Launched: {os.path.basename(file)}")
            def monitor():
                proc.wait()
                add_log("MPV Closed. Auto-Cleanup...")
                self.sync()
            Thread(target=monitor, daemon=True).start()
            time.sleep(1.5); return self.sync()
        except: return {"status": "error"}

class MeetServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    def __init__(self, addr, handler):
        self.engine = MeetEngine()
        super().__init__(addr, handler)

if __name__ == "__main__":
    add_log("MeetShare Engine Fixed")
    with MeetServer(("0.0.0.0", PORT), FastAPIHandler) as httpd:
        httpd.serve_forever()
