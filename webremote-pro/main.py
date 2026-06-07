import http.server
import json
import os
import subprocess
import urllib.parse
import socketserver
import socket

PORT = 5000
SOCKET_PATH = "/run/user/1000/.ydotool_socket"

class WebRemoteHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Allow CORS and private networks
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path.startswith('/api/'):
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b''
            try:
                data = json.loads(post_data.decode('utf-8')) if post_data else {}
            except json.JSONDecodeError:
                data = {}

            response = self.handle_api(parsed_path.path, data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

    def handle_api(self, path, data):
        env = os.environ.copy()
        if 'YDOTOOL_SOCKET' not in env:
            env['YDOTOOL_SOCKET'] = SOCKET_PATH

        if path == '/api/mouse/move':
            x = int(data.get('x', 0))
            y = int(data.get('y', 0))
            subprocess.run(['ydotool', 'mousemove', '--', str(x), str(y)], env=env)
            return {"status": "ok"}

        elif path == '/api/mouse/click':
            btn = data.get('button', 'left')
            code = "0xC0" # left
            if btn == 'right': code = "0xC1"
            elif btn == 'middle': code = "0xC2"
            subprocess.run(['ydotool', 'click', code], env=env)
            return {"status": "ok"}

        elif path == '/api/mouse/scroll':
            y = int(data.get('y', 0))
            subprocess.run(['ydotool', 'mousemove', '-w', '-y', str(y)], env=env)
            return {"status": "ok"}

        elif path == '/api/keyboard/key':
            key = data.get('key', '')
            key_map = {
                'enter': '28',
                'backspace': '14',
                'space': '57',
                'esc': '1',
                'tab': '15',
                'super': '125',
                'up': '103',
                'down': '108',
                'left': '105',
                'right': '106'
            }
            code = key_map.get(key)
            if code:
                subprocess.run(['ydotool', 'key', f"{code}:1", f"{code}:0"], env=env)
                return {"status": "ok"}
            return {"status": "error", "message": f"Unknown key {key}"}

        elif path == '/api/keyboard/type':
            text = data.get('text', '')
            if text:
                subprocess.run(['ydotool', 'type', text], env=env)
            return {"status": "ok"}

        elif path == '/api/media/control':
            action = data.get('action', '')
            key_map = {
                'mute': '113',
                'volume_down': '114',
                'volume_up': '115',
                'play_pause': '164',
                'next': '163',
                'prev': '165'
            }
            code = key_map.get(action)
            if code:
                subprocess.run(['ydotool', 'key', f"{code}:1", f"{code}:0"], env=env)
                return {"status": "ok"}
            return {"status": "error", "message": f"Unknown media action {action}"}

        elif path == '/api/system/control':
            action = data.get('action', '')
            if action == 'lock':
                # Attempt to lock the session using standard methods
                subprocess.run(['loginctl', 'lock-session'])
                return {"status": "ok"}
            elif action == 'suspend':
                subprocess.run(['systemctl', 'suspend'])
                return {"status": "ok"}
            elif action == 'poweroff':
                subprocess.run(['systemctl', 'poweroff'])
                return {"status": "ok"}
            elif action == 'reboot':
                subprocess.run(['systemctl', 'reboot'])
                return {"status": "ok"}
            return {"status": "error", "message": "Unknown action"}

        elif path == '/api/status':
            try:
                vol_out = subprocess.check_output(['wpctl', 'get-volume', '@DEFAULT_AUDIO_SINK@']).decode('utf-8').strip()
            except:
                vol_out = "Unknown"
            return {"status": "ok", "volume": vol_out}

        return {"status": "error", "message": "Unknown API path"}

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/':
            self.path = '/index.html'
        return super().do_GET()

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"Starting Web Remote Pro on http://{get_ip()}:{PORT}")
    with ThreadingHTTPServer(("0.0.0.0", PORT), WebRemoteHandler) as httpd:
        httpd.serve_forever()
