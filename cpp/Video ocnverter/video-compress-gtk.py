#!/usr/bin/env python3

import gi
import os
import subprocess
import signal
import json
import threading
import shutil
import re
import sys
import glob
import atexit
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk, Pango, GdkPixbuf

# ─── CONSTANTS ───
APP_NAME = "video-converter"
CONFIG_DIR = Path.home() / ".config" / APP_NAME
CONFIG_PATH = CONFIG_DIR / "config.json"
CACHE_DIR = Path.home() / ".cache" / APP_NAME
OUTPUT_DIR_NAME = "Video converter output"

# Drag Target
TARGET_ENTRY = Gtk.TargetEntry.new("ROW_DND", Gtk.TargetFlags.SAME_APP, 0)

THUMB_POOL = ThreadPoolExecutor(max_workers=4)
VIDEO_EXTS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv", ".m4v", ".mts", ".m2ts", ".ts"}

CODECS = {
    "HEVC (VAAPI 10-bit)":   {"name": "hevc_vaapi", "fmt": "p010", "type": "vaapi"},
    "HEVC (Standard 8-bit)": {"name": "hevc_vaapi", "fmt": "nv12", "type": "vaapi"},
    "AV1 (VAAPI 10-bit)":    {"name": "av1_vaapi",  "fmt": "p010", "type": "vaapi"},
    "AV1 (CPU - SVT-AV1)":   {"name": "libsvtav1",  "fmt": "yuv420p10le", "type": "cpu"},
}

# ─── QUALITY MAPS ───

QUALITY_MAP_GPU = {
    "Best - 90% (QV-18)": 18,
    "High - 70% (QV-22)": 22,
    "Main - 50% (QV-26)": 26,
    "Lite - 30% (QV-30)": 30,
    "Tiny - 20% (QV-34)": 34
}

# Corresponding multipliers
BITRATE_MULTIPLIER_MAP = {
    18: 0.9,  # Best
    22: 0.7,  # High
    26: 0.5,  # Main
    30: 0.3,  # Lite
    34: 0.2   # Tiny
}

QUALITY_MAP_CPU = {
    "Preset 4 (Best Size)": 4, "Preset 5 (Very Slow)": 5,
    "Preset 6 (Balanced)": 6, "Preset 7 (Faster)": 7,
    "Preset 8 (Fast)": 8, "Preset 9 (Very Fast)": 9,
    "Preset 10 (Super Fast)": 10
}

AUTO_CLOSE_MAP = {"Never": 0, "After 1 min": 60, "After 5 min": 300}
AFTER_ACTIONS = ("Keep source", "Move to Trash", "Delete permanently")
AFTER_COMPLETE = ("Do nothing", "Shutdown system")


# ─── LOGIC HELPERS ───

def ui(fn, *args):
    """Safe wrapper to run UI updates from threads."""
    GLib.idle_add(fn, *args)

def check_dependencies():
    dependency_map = {"ffmpeg": "ffmpeg", "ffprobe": "ffmpeg", "trash-put": "trash-cli"}
    missing = {pkg for bin_name, pkg in dependency_map.items() if shutil.which(bin_name) is None}
    if missing:
        try: subprocess.check_call(["pkexec", "pacman", "-S", "--needed", "--noconfirm"] + list(missing))
        except subprocess.CalledProcessError: sys.exit(f"Missing: {missing}")
    if shutil.which("udevadm") is None: print("Warning: 'udevadm' missing.")
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        for f in CACHE_DIR.glob("*.jpg"): 
            try: f.unlink() 
            except: pass
    except: pass

class ConfigManager:
    @staticmethod
    def load():
        try: return json.loads(CONFIG_PATH.read_text())
        except: return {}
    @staticmethod
    def save(cfg):
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            CONFIG_PATH.write_text(json.dumps(cfg, indent=2))
        except: pass

def build_ffmpeg_command(file, out, codec_conf, val, device_path, do_scale, input_codec, target_bitrate, max_bitrate):
    is_cpu = (codec_conf["type"] == "cpu")
    force_cpu_decode = (input_codec == "av1" and not is_cpu)
    
    # 3️⃣ FFmpeg Efficiency: Added -hide_banner to clean up parsing
    cmd = ["ffmpeg", "-y", "-progress", "pipe:2", "-hide_banner"]
    
    if not is_cpu:
        cmd.extend(["-init_hw_device", f"vaapi=va:{device_path}", "-filter_hw_device", "va"])
        if not force_cpu_decode: cmd.extend(["-hwaccel", "vaapi", "-hwaccel_output_format", "vaapi", "-extra_hw_frames", "256"])
    
    cmd.extend(["-i", file])
    
    vf_chain = []
    if is_cpu:
        if do_scale: vf_chain.append("scale='min(1920,iw)':-2")
        vf_chain.append(f"format={codec_conf['fmt']}")
    else:
        if force_cpu_decode: vf_chain.append("format=nv12|p010,hwupload")
        if do_scale: vf_chain.append(f"scale_vaapi=w='min(1920,iw)':h=-2:format={codec_conf['fmt']}")
        else: vf_chain.append(f"scale_vaapi=format={codec_conf['fmt']}")
    
    if vf_chain: cmd.extend(["-vf", ",".join(vf_chain)])
    cmd.extend(["-c:v", codec_conf["name"]])
    
    if is_cpu:
        cmd.extend(["-crf", "26", "-preset", str(val)])
    else:
        # Kept QVBR as requested (Not ICQ)
        cmd.extend(["-compression_level", "1"])
        buf_size = max_bitrate * 2
        cmd.extend([
            "-rc_mode", "QVBR",
            "-global_quality", str(val),
            "-b:v", str(target_bitrate),
            "-maxrate", str(max_bitrate),
            "-bufsize", str(buf_size)
        ])
    
    cmd.extend(["-c:a", "copy", "-c:s", "copy", "-map_metadata", "0", "-avoid_negative_ts", "1", out])
    return cmd

# ─── ROBUST PROGRESS PARSER ───

class ProgressParser:
    def __init__(self, duration):
        self.duration_us = duration * 1_000_000
        self.state = {}
        self.start_time = time.time()

    def parse(self, line):
        line = line.strip()
        if "=" not in line: return None
        
        key, val = line.split("=", 1)
        key = key.strip(); val = val.strip()
        self.state[key] = val

        if key == "progress" and val == "continue":
            try:
                out_time_us = int(self.state.get("out_time_us", 0))
                pct = min(out_time_us / self.duration_us, 0.99) if self.duration_us > 0 else 0
                fps = float(self.state.get("fps", 0))
                
                speed_str = self.state.get("speed", "0")
                speed = float(speed_str.replace("x", "")) if "x" in speed_str else float(speed_str)
                
                br_str = self.state.get("bitrate", "0")
                bitrate = float(br_str.replace("kbits/s", "")) if "N/A" not in br_str else 0

                elapsed = time.time() - self.start_time
                rem = (elapsed / pct - elapsed) if pct > 0 else 0
                return pct, fps, speed, bitrate, rem
            except: return None
        return None

# ─── UI CLASSES ───

class SleepInhibitor:
    def __init__(self): self._proc = None
    def start(self):
        if not self._proc:
            try: self._proc = subprocess.Popen(["systemd-inhibit", "--what=idle", "--who=VideoConverter", "--why=Encoding", "sleep", "infinity"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except: pass
    def stop(self):
        if self._proc: self._proc.terminate(); self._proc = None

class FileRow:
    __slots__ = ('path', 'id', 'root', 'label', 'remove_btn', 'play_btn', 'progress', 'info', 'conflict', 'thumb', 'log_btn', 'log_data', 'pulse_id')

    def __init__(self, path_str, remove_cb, move_up_cb, move_down_cb):
        self.path = Path(path_str)
        self.id = path_str 
        self.log_data = [] 
        self.pulse_id = None
        
        frame = Gtk.Frame()
        frame.get_style_context().add_class("row-card")
        self.root = frame 

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        hbox.set_border_width(8)
        frame.add(hbox)

        # Arrows
        arrows_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        arrows_box.set_valign(Gtk.Align.CENTER)
        
        up_btn = Gtk.Button.new_from_icon_name("go-up-symbolic", Gtk.IconSize.MENU)
        up_btn.get_style_context().add_class("flat-button")
        up_btn.connect("clicked", lambda _: move_up_cb(self.id))
        
        down_btn = Gtk.Button.new_from_icon_name("go-down-symbolic", Gtk.IconSize.MENU)
        down_btn.get_style_context().add_class("flat-button")
        down_btn.connect("clicked", lambda _: move_down_cb(self.id))
        
        arrows_box.pack_start(up_btn, False, False, 0)
        arrows_box.pack_start(down_btn, False, False, 0)
        hbox.pack_start(arrows_box, False, False, 0)

        self.thumb = Gtk.Image.new_from_icon_name("video-x-generic-symbolic", Gtk.IconSize.DIALOG)
        self.thumb.set_pixel_size(48)
        self.thumb.get_style_context().add_class("thumbnail")
        self.thumb.set_size_request(96, 54)
        hbox.pack_start(self.thumb, False, False, 0)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        hbox.pack_start(content_box, True, True, 0)

        top_line = Gtk.Box(spacing=6)
        content_box.pack_start(top_line, False, False, 0)

        self.label = Gtk.Label(xalign=0, label=self.path.name)
        self.label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        top_line.pack_start(self.label, True, True, 0)

        self.conflict = Gtk.Label()
        self.conflict.set_no_show_all(True)
        top_line.pack_start(self.conflict, False, False, 0)

        self.info = Gtk.Label(xalign=0, label="Pending...")
        self.info.set_use_markup(True)
        self.info.get_style_context().add_class("dim-label")
        content_box.pack_start(self.info, False, False, 0)

        self.progress = Gtk.ProgressBar()
        self.progress.set_hexpand(True)
        content_box.pack_start(self.progress, False, False, 0)

        action_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        action_box.set_valign(Gtk.Align.CENTER)
        
        self.remove_btn = Gtk.Button.new_from_icon_name("user-trash-symbolic", Gtk.IconSize.BUTTON)
        self.remove_btn.get_style_context().add_class("row-remove-btn")
        self.remove_btn.connect("clicked", lambda _: remove_cb(self.id))
        
        self.play_btn = Gtk.Button.new_from_icon_name("media-playback-start-symbolic", Gtk.IconSize.BUTTON)
        self.play_btn.set_no_show_all(True) 
        
        self.log_btn = Gtk.Button.new_from_icon_name("dialog-warning-symbolic", Gtk.IconSize.BUTTON)
        self.log_btn.set_no_show_all(True)
        self.log_btn.get_style_context().add_class("destructive-action")
        self.log_btn.connect("clicked", self.show_log)

        action_box.pack_start(self.play_btn, False, False, 0)
        action_box.pack_start(self.log_btn, False, False, 0)
        action_box.pack_start(self.remove_btn, False, False, 0)
        hbox.pack_end(action_box, False, False, 0)

        THUMB_POOL.submit(self._generate_thumb)

    def show_log(self, btn):
        dialog = Gtk.Dialog(title="FFmpeg Log", flags=0)
        dialog.add_buttons("Copy", 1, "Clear", 2, "Close", Gtk.ResponseType.CLOSE)
        dialog.set_default_size(700, 500)
        
        box = dialog.get_content_area()
        box.set_spacing(10); box.set_border_width(10)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_hexpand(True); scrolled.set_vexpand(True)
        box.add(scrolled)
        
        text_view = Gtk.TextView()
        text_view.set_editable(False)
        text_view.set_monospace(True)
        text_view.get_buffer().set_text("\n".join(self.log_data))
        scrolled.add(text_view)
        
        dialog.show_all()
        while True:
            response = dialog.run()
            if response == 1: 
                clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
                clipboard.set_text("\n".join(self.log_data), -1)
            elif response == 2: self.log_data.clear(); text_view.get_buffer().set_text("")
            else: break
        dialog.destroy()

    def _generate_thumb(self):
        try:
            thumb = CACHE_DIR / f"{abs(hash(str(self.path)))}.jpg"
            if not thumb.exists():
                subprocess.run(["ffmpeg", "-ss", "5", "-i", str(self.path), "-vframes", "1", "-vf", "scale=192:-1", "-q:v", "5", str(thumb)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            GLib.idle_add(self._set_thumb, str(thumb))
        except: pass

    def _set_thumb(self, path):
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, 96, 54, True)
            self.thumb.set_from_pixbuf(pixbuf)
        except: pass

    def set_active(self, active):
        ctx = self.root.get_style_context()
        if active: ctx.add_class("active-row")
        else: ctx.remove_class("active-row")

    def show_conflict(self):
        self.conflict.set_markup("<span foreground='#f39c12' weight='bold' size='small'>⚠ Overwrite</span>")
        self.conflict.show()
        
    def set_success(self):
        self.progress.get_style_context().add_class("success-bar")

class VideoConverter(Gtk.Window):
    def __init__(self):
        super().__init__(title="Video Converter")
        self.set_default_size(950, 650)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", self.on_quit_attempt)
        atexit.register(self.cleanup)

        self.config = ConfigManager.load()
        self.files = []
        self.processed_files = set() 
        self.rows = {}
        self.file_info_cache = {} 
        self.proc = None
        self.current_file = None
        self.stop_requested = False
        self.paused = False
        self.last_output_dir = None
        self.countdown_source_id = None 
        self.inhibitor = SleepInhibitor()
        self.last_folder = self.config.get("last_folder", None)
        self.sidebar_visible = True 
        self.active_quality_map = QUALITY_MAP_GPU

        self._init_ui()
        self._init_shortcuts()
        self._load_static_css()
        self._update_empty_state()
        self.on_codec_changed(self.codec)

    def on_quit_attempt(self, widget, event):
        if self.proc:
            dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.WARNING,
                                     buttons=Gtk.ButtonsType.YES_NO, text="Encoding in Progress")
            dialog.format_secondary_text("Are you sure you want to quit?")
            if dialog.run() == Gtk.ResponseType.YES: self.cleanup(); Gtk.main_quit()
            dialog.destroy()
            return True
        Gtk.main_quit()
        return False

    def cleanup(self):
        if self.proc:
            try: self.proc.terminate(); self.proc.wait(timeout=1)
            except: self.proc.kill()
        self.inhibitor.stop()
        THUMB_POOL.shutdown(wait=False)

    def _get_render_devices(self):
        devs = glob.glob("/dev/dri/renderD*")
        devs.sort()
        devices = []
        for d in devs:
            label = os.path.basename(d)
            try:
                u = subprocess.check_output(["udevadm", "info", "-a", "-n", d], text=True)
                if "0x1002" in u: label = f"AMD ({label})"
                elif "0x8086" in u: label = f"Intel ({label})"
                elif "0x10de" in u: label = f"NVIDIA ({label})"
            except: pass
            devices.append((d, label))
        return devices if devices else [("", "No VAAPI Device")]

    def _init_ui(self):
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.props.title = "Video Converter"
        self.set_titlebar(header)

        self.hamburger_btn = Gtk.Button.new_from_icon_name("open-menu-symbolic", Gtk.IconSize.MENU)
        self.hamburger_btn.connect("clicked", lambda _: self.toggle_sidebar(not self.sidebar_visible))
        header.pack_start(self.hamburger_btn)

        self.overlay = Gtk.Overlay()
        self.add(self.overlay)

        main_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.overlay.add(main_hbox)

        self.sidebar_revealer = Gtk.Revealer()
        self.sidebar_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_RIGHT)
        self.sidebar_revealer.set_transition_duration(250)
        self.sidebar_revealer.set_reveal_child(True) 
        main_hbox.pack_start(self.sidebar_revealer, False, False, 0)

        sidebar_frame = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar_frame.set_size_request(200, -1) 
        sidebar_frame.get_style_context().add_class("sidebar-bg")
        self.sidebar_revealer.add(sidebar_frame)

        header_box = Gtk.Box(spacing=10)
        header_box.set_border_width(12)
        app_title = Gtk.Label(xalign=0)
        app_title.set_markup("<span weight='heavy' size='large'>Configuration</span>")
        header_box.pack_start(app_title, True, True, 0)
        sidebar_frame.pack_start(header_box, False, False, 0)

        side_scroll = Gtk.ScrolledWindow()
        side_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sidebar_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        sidebar_content.set_border_width(15)
        side_scroll.add(sidebar_content)
        sidebar_frame.pack_start(side_scroll, True, True, 0)

        self.gpu_device = Gtk.ComboBoxText()
        for path, label in self._get_render_devices(): 
            self.gpu_device.append(path, label)
        self.gpu_device.set_active(0) 
        self._add_field(sidebar_content, "GPU Device", self.gpu_device)

        self.codec = self._combo(list(CODECS.keys()), "codec", 0)
        self.codec.connect("changed", self.on_codec_changed)
        self._add_field(sidebar_content, "Codec", self.codec)
        
        self.quality = Gtk.ComboBoxText()
        self._add_field(sidebar_content, "Quality / Preset", self.quality)
        
        self.scale_chk = Gtk.Switch()
        self.scale_chk.set_active(True)
        self.scale_chk.set_halign(Gtk.Align.START)
        self._add_field(sidebar_content, "Limit to 1080p", self.scale_chk)
        
        self.after_action = self._combo(AFTER_ACTIONS, "after_action", 0)
        self._add_field(sidebar_content, "Handling", self.after_action)
        self.auto_close = self._combo(AUTO_CLOSE_MAP, "auto_close", 0)
        self._add_field(sidebar_content, "Auto Close", self.auto_close)
        self.after_complete = self._combo(AFTER_COMPLETE, "after_complete", 0)
        self._add_field(sidebar_content, "Completion", self.after_complete)

        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_hbox.pack_start(right_box, True, True, 0)

        # Top Control Bar
        top_controls = Gtk.Box(spacing=10)
        top_controls.set_border_width(12)
        top_controls.set_margin_bottom(0)
        right_box.pack_start(top_controls, False, False, 0)

        self.open_out_btn = Gtk.Button.new_from_icon_name("folder-open-symbolic", Gtk.IconSize.BUTTON)
        self.open_out_btn.set_sensitive(False)
        self.open_out_btn.set_tooltip_text("Open Output Folder")
        self.open_out_btn.connect("clicked", self.open_output_folder)
        top_controls.pack_start(self.open_out_btn, False, False, 0)

        self.add_btn = Gtk.Button.new_from_icon_name("list-add-symbolic", Gtk.IconSize.BUTTON)
        self.add_btn.get_style_context().add_class("suggested-action")
        self.add_btn.set_tooltip_text("Add Videos")
        self.add_btn.connect("clicked", self.pick_files)
        top_controls.pack_start(self.add_btn, False, False, 0)

        clear_btn = Gtk.Button.new_from_icon_name("edit-clear-all-symbolic", Gtk.IconSize.BUTTON)
        clear_btn.set_tooltip_text("Clear List")
        clear_btn.connect("clicked", self.clear_all)
        top_controls.pack_end(clear_btn, False, False, 0)

        right_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0)

        # List Area
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        right_box.pack_start(self.stack, True, True, 0)

        self.empty_state = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.empty_state.set_valign(Gtk.Align.CENTER)
        self.empty_state.set_halign(Gtk.Align.CENTER)
        icon = Gtk.Image.new_from_icon_name("video-x-generic-symbolic", Gtk.IconSize.DIALOG)
        icon.set_pixel_size(96); icon.set_opacity(0.3)
        lbl = Gtk.Label(); lbl.set_markup("<span size='xx-large' weight='bold' foreground='#555555'>Drop Videos Here</span>")
        self.empty_state.pack_start(icon, False, False, 0)
        self.empty_state.pack_start(lbl, False, False, 0)
        self.stack.add_named(self.empty_state, "empty")

        list_scroll = Gtk.ScrolledWindow()
        list_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.listbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.listbox.set_border_width(12)
        list_scroll.add(self.listbox)
        self.stack.add_named(list_scroll, "list")

        self.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        self.drag_dest_add_uri_targets()
        self.connect("drag-data-received", self.on_drag_data_received)
        self.connect("drag-motion", self.on_drag_motion)
        self.connect("drag-leave", self.on_drag_leave)

        # Bottom Control Bar
        controls_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        controls_area.get_style_context().add_class("bottom-bar")
        controls_area.set_border_width(12)
        right_box.pack_end(controls_area, False, False, 0)
        right_box.pack_end(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0)

        self.queue_status = Gtk.Label(label="Ready.")
        self.queue_status.set_use_markup(True)
        self.queue_status.set_justify(Gtk.Justification.LEFT) 
        self.queue_status.set_xalign(0)
        self.queue_status.set_ellipsize(Pango.EllipsizeMode.END)
        self.queue_status.set_max_width_chars(30)
        controls_area.pack_start(self.queue_status, True, True, 0) 

        self.start_btn = Gtk.Button.new_from_icon_name("media-playback-start-symbolic", Gtk.IconSize.BUTTON)
        self.start_btn.get_style_context().add_class("suggested-action")
        self.start_btn.set_tooltip_text("Start Queue")
        self.start_btn.set_valign(Gtk.Align.CENTER)
        self.start_btn.connect("clicked", self.start)
        controls_area.pack_end(self.start_btn, False, False, 0) 

        self.pause_btn = Gtk.Button.new_from_icon_name("media-playback-pause-symbolic", Gtk.IconSize.BUTTON)
        self.pause_btn.set_sensitive(False)
        self.pause_btn.set_tooltip_text("Pause")
        self.pause_btn.set_valign(Gtk.Align.CENTER)
        self.pause_btn.connect("clicked", self.pause_resume)
        controls_area.pack_end(self.pause_btn, False, False, 0) 

        stop_btn = Gtk.Button.new_from_icon_name("media-playback-stop-symbolic", Gtk.IconSize.BUTTON)
        stop_btn.get_style_context().add_class("destructive-action") 
        stop_btn.set_tooltip_text("Stop Queue")
        stop_btn.set_valign(Gtk.Align.CENTER)
        stop_btn.connect("clicked", self.stop)
        controls_area.pack_end(stop_btn, False, False, 0) 

    def _init_shortcuts(self):
        self.connect("key-press-event", self.on_key_press)
        
    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_o and (event.state & Gdk.ModifierType.CONTROL_MASK):
            self.pick_files(None); return True
        if event.keyval == Gdk.KEY_q and (event.state & Gdk.ModifierType.CONTROL_MASK):
            self.on_quit_attempt(self, None); return True
        if event.keyval in [Gdk.KEY_Return, Gdk.KEY_KP_Enter] and (event.state & Gdk.ModifierType.CONTROL_MASK):
            if self.files and not self.proc: self.start(None)
            return True
        return False

    def toggle_sidebar(self, show):
        self.sidebar_revealer.set_reveal_child(show)
        self.sidebar_visible = show
        self.queue_draw() 

    def _update_empty_state(self):
        if self.files: self.stack.set_visible_child_name("list")
        else: self.stack.set_visible_child_name("empty")
        self.start_btn.set_sensitive(len(self.files) > 0)

    def _add_field(self, container, label_text, widget):
        lbl = Gtk.Label(label=label_text.upper(), xalign=0)
        lbl.get_style_context().add_class("dim-label")
        container.pack_start(lbl, False, False, 0)
        container.pack_start(widget, False, False, 0)

    def _combo(self, values, config_key, default_val):
        c = Gtk.ComboBoxText()
        for v in values: c.append_text(v)
        c.set_active(self.config.get(config_key, default_val))
        return c

    def on_codec_changed(self, combo):
        codec_key = combo.get_active_text()
        if not codec_key: return
        if "CPU" in codec_key:
            new_map = QUALITY_MAP_CPU
            default_val = 6 # Default to Balanced CPU
        else:
            new_map = QUALITY_MAP_GPU
            default_val = 26 # Default to Main (26) GPU

        self.active_quality_map = new_map
        self.quality.remove_all()
        sorted_items = sorted(new_map.items(), key=lambda item: item[1])
        for k, v in sorted_items: self.quality.append_text(k)
        
        self.quality.set_active(0)
        for i, (k, v) in enumerate(sorted_items):
             if v == default_val: self.quality.set_active(i); break

    def _filesize(self, path):
        try: return os.path.getsize(path)
        except: return 0

    def _human_size(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0: return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}PB"

    def _open_folder_safe(self, path):
        if not path or not os.path.exists(path): return
        managers = ["dolphin", "thunar", "nautilus", "nemo", "pcmanfm", "caja"]
        for fm in managers:
            if shutil.which(fm): subprocess.Popen([fm, path]); return
        subprocess.Popen(["xdg-open", path])

    def open_output_folder(self, _):
        if self.last_output_dir: self._open_folder_safe(self.last_output_dir)

    def send_notification(self, title, body):
        try: subprocess.run(["notify-send", "-a", APP_NAME, title, body])
        except: pass

    def on_drag_motion(self, widget, context, x, y, time):
        self.stack.get_style_context().add_class("drag-active")
        Gdk.drag_status(context, Gdk.DragAction.COPY, time)
        return True

    def on_drag_leave(self, widget, context, time):
        self.stack.get_style_context().remove_class("drag-active")

    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        self.stack.get_style_context().remove_class("drag-active")
        uris = data.get_uris()
        paths = []
        for uri in uris:
            try:
                path_str, _ = GLib.filename_from_uri(uri)
                path = Path(path_str)
                if path.is_file() and path.suffix.lower() in VIDEO_EXTS: paths.append(str(path))
                elif path.is_dir():
                    for root, _, files in os.walk(path):
                        for name in files:
                            sub_path = Path(root) / name
                            if sub_path.suffix.lower() in VIDEO_EXTS: paths.append(str(sub_path))
            except: continue
        if paths: self.add_files(paths)
        # 1️⃣ Drag-and-Drop Fix: Ensure delete=False to prevent ANY source modification
        Gtk.drag_finish(drag_context, True, False, time)

    def add_files(self, paths):
        for f in paths:
            if f not in self.rows:
                self.files.append(f)
                row = FileRow(f, self.remove_file, self.move_row_up, self.move_row_down)
                self.rows[f] = row
                self.listbox.pack_start(row.root, False, False, 0)
        self.show_all()
        self._update_empty_state()

    def move_row_up(self, file_id):
        try:
            idx = self.files.index(file_id)
            if idx > 0:
                self.files[idx], self.files[idx-1] = self.files[idx-1], self.files[idx]
                row = self.rows[file_id].root
                self.listbox.reorder_child(row, idx - 1)
        except ValueError: pass

    def move_row_down(self, file_id):
        try:
            idx = self.files.index(file_id)
            if idx < len(self.files) - 1:
                self.files[idx], self.files[idx+1] = self.files[idx+1], self.files[idx]
                row = self.rows[file_id].root
                self.listbox.reorder_child(row, idx + 1)
        except ValueError: pass

    def pick_files(self, _):
        dlg = Gtk.FileChooserDialog(title="Select Videos", parent=self, action=Gtk.FileChooserAction.OPEN)
        dlg.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        dlg.set_select_multiple(True)
        if self.last_folder: dlg.set_current_folder(self.last_folder)
        if dlg.run() == Gtk.ResponseType.OK:
            self.last_folder = dlg.get_current_folder()
            ConfigManager.save(self._gather_prefs())
            self.add_files([x.get_path() for x in dlg.get_files()])
        dlg.destroy()

    def remove_file(self, path):
        if path == self.current_file and self.proc: return
        if path in self.files: self.files.remove(path)
        if path in self.file_info_cache: del self.file_info_cache[path]
        if path in self.rows: self.listbox.remove(self.rows.pop(path).root)
        self._update_empty_state()

    def clear_all(self, _):
        if self.proc: return 
        for f in list(self.files): self.remove_file(f)

    def start(self, _):
        if not self.files or self.proc: return
        ConfigManager.save(self._gather_prefs())
        self.pause_btn.set_sensitive(True)
        self.open_out_btn.set_sensitive(True)
        self.stop_requested = False
        threading.Thread(target=self.encode_all, daemon=True).start()

    def pause_resume(self, _):
        if self.proc:
            self.proc.send_signal(signal.SIGCONT if self.paused else signal.SIGSTOP)
            self.paused = not self.paused
            icon_name = "media-playback-start-symbolic" if self.paused else "media-playback-pause-symbolic"
            self.pause_btn.set_image(Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON))
            self.pause_btn.set_tooltip_text("Resume" if self.paused else "Pause")

    def stop(self, _):
        self.stop_requested = True
        if self.countdown_source_id:
            GLib.source_remove(self.countdown_source_id)
            self.countdown_source_id = None
            self.queue_status.set_text("⚠ Canceled.")
        if self.proc: self.proc.send_signal(signal.SIGTERM)

    def _get_out_path(self, src):
        val = self.active_quality_map.get(self.quality.get_active_text(), 26)
        # Suffix remains QVBR as requested
        suffix = f"preset{val}" if val < 13 else f"qvbr{val}"
        src_dir = os.path.dirname(src)
        out_dir = src_dir
        if sum(1 for f in self.files if os.path.dirname(f) == src_dir) > 1:
            out_dir = os.path.join(src_dir, OUTPUT_DIR_NAME)
            os.makedirs(out_dir, exist_ok=True)
        self.last_output_dir = out_dir
        return str(Path(out_dir) / f"{Path(src).stem}_comp_{suffix}.mkv")

    def _update_row_ui(self, row, pct, fps, speed, bitrate, rem, q_rem, init_size_str, est_size_str):
        if hasattr(row, 'pulse_id') and row.pulse_id:
             GLib.source_remove(row.pulse_id); row.pulse_id = None

        row.progress.set_fraction(pct)
        markup = (f"<span size='large'><b>{int(pct*100)}%</b> • <span foreground='#2ec27e'><b>{fps:.0f} fps</b></span> • <span foreground='#62a0ea'>x{speed:.1f}</span> • "
                  f"<span foreground='#ffb74d'><b>ETA: {self.fmt_time(rem)}</b></span></span>\n"
                  f"<span size='medium' alpha='80%'>{init_size_str} ➝ <span foreground='#c061cb'>{est_size_str}</span></span>")
        row.info.set_markup(markup)
        bitrate_str = f"{bitrate:.0f} kbps" if bitrate > 0 else "N/A"
        self.queue_status.set_markup(
            f"<span size='medium' weight='bold' foreground='#ffb74d'>Queue ETA: {self.fmt_time(q_rem)}</span>\n"
            f"<span size='medium' weight='bold' foreground='#2ec27e'>Bitrate: {bitrate_str}</span>"
        )

    def get_file_info(self, f):
        try:
            cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "format=duration,bit_rate:stream=r_frame_rate,codec_name", "-of", "json", f]
            out = subprocess.check_output(cmd, timeout=2, text=True)
            data = json.loads(out)
            
            dur = float(data['format'].get('duration', 1.0))
            src_bitrate = float(data['format'].get('bit_rate', 5_000_000))
            
            fps_str = data['streams'][0].get('r_frame_rate', "30/1")
            fps = float(fps_str.split('/')[0]) / float(fps_str.split('/')[1]) if '/' in fps_str else float(fps_str)
            codec = data['streams'][0].get('codec_name', "unknown")
            
            return dur, fps, codec, src_bitrate
        except: return 1.0, 30.0, "unknown", 5_000_000

    def encode_all(self):
        self.inhibitor.start()
        for f in self.files:
            if os.path.exists(self._get_out_path(f)): ui(self.rows[f].show_conflict)
            if f not in self.file_info_cache: self.file_info_cache[f] = self.get_file_info(f)

        while True:
            if self.stop_requested: break
            next_file = None
            future_sec = 0
            for f in self.files:
                if f not in self.processed_files:
                    if next_file is None: next_file = f
                    else: future_sec += self.file_info_cache.get(f, (0,0,0,0))[0]
            if next_file is None: break
            self.current_file = next_file
            for r in self.rows.values(): ui(r.set_active, False)
            ui(self.rows[next_file].set_active, True)
            
            if self.encode_file(next_file, future_sec) and not self.stop_requested:
                self._handle_source_action(next_file)
                self.processed_files.add(next_file)
            else:
                if self.stop_requested: break
                self.processed_files.add(next_file)

        self.inhibitor.stop()
        self.current_file = None
        self.processed_files.clear() 
        ui(lambda: (self.queue_status.set_markup(f"<span size='x-large' weight='bold' foreground='#{'ff5555' if self.stop_requested else '2ec27e'}'>{'⚠ Batch Canceled' if self.stop_requested else '✔ Queue Completed'}</span>"), self.pause_btn.set_sensitive(False)))
        if not self.stop_requested: self._handle_completion()

    def encode_file(self, file, future_sec=0):
        row = self.rows[file]
        row.log_data.clear() 
        ui(lambda: row.info.set_text("Initializing..."))
        row.pulse_id = None
        def _pulse(): row.progress.pulse(); return True
        GLib.idle_add(lambda: setattr(row, 'pulse_id', GLib.timeout_add(100, _pulse)))

        dur, src_fps, input_codec, src_bitrate = self.file_info_cache.get(file, (1.0, 30.0, 'unknown', 5_000_000))
        
        out = self._get_out_path(file)
        codec_key = self.codec.get_active_text()
        if codec_key not in CODECS: codec_key = list(CODECS.keys())[0]
        device_path = self.gpu_device.get_active_id()
        if not device_path: device_path = "/dev/dri/renderD128"
        
        val = self.active_quality_map.get(self.quality.get_active_text(), 26)
        multiplier = BITRATE_MULTIPLIER_MAP.get(val, 0.5)
        
        target_k = max(int(src_bitrate * multiplier), 300_000)
        maxrate_k = max(int(target_k * 1.5), 600_000)

        cmd = build_ffmpeg_command(
            file, out, 
            CODECS[codec_key], 
            val, 
            device_path, 
            self.scale_chk.get_active(), 
            input_codec, 
            target_k, 
            maxrate_k
        )
        
        ui(self.queue_status.set_text, f"Processing: {os.path.basename(file)}...")
        init_size = self._filesize(file)
        init_size_str = self._human_size(init_size)
        
        parser = ProgressParser(dur)

        try:
            self.proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, text=True, bufsize=1)
            
            while self.proc.poll() is None:
                line = self.proc.stderr.readline()
                if not line: continue
                
                row.log_data.append(line.strip())
                if len(row.log_data) > 300: row.log_data.pop(0)

                stats = parser.parse(line)
                if stats:
                    pct, fps, speed, bitrate, rem = stats
                    q_rem = rem + (future_sec / max(speed, 0.001))
                    est_size_str = "?"
                    if bitrate > 0: est_size_str = self._human_size((bitrate * 1000 / 8) * dur)
                    GLib.idle_add(self._update_row_ui, row, pct, fps, speed, bitrate, rem, q_rem, init_size_str, est_size_str)
                    
            return_code = self.proc.returncode
        except Exception as e: 
            row.log_data.append(str(e))
            return_code = 1
        
        def cleanup_pulse():
            if hasattr(row, 'pulse_id') and row.pulse_id is not None:
                GLib.source_remove(row.pulse_id)
                row.pulse_id = None
        GLib.idle_add(cleanup_pulse)

        self.proc = None
        if return_code == 0:
            saved = (1 - self._filesize(out) / self._filesize(file)) * 100 if self._filesize(file) else 0
            markup = (f"<span foreground='#2ec27e'><b>✔ COMPLETED</b></span>\n"
                      f"<span size='small' alpha='60%'>Saved {saved:.0f}%  •  {self._human_size(self._filesize(out))}</span>")
            GLib.idle_add(lambda: (
                row.set_active(False), row.set_success(),
                row.progress.set_fraction(1.0), row.info.set_markup(markup), 
                row.play_btn.connect("clicked", lambda _: subprocess.Popen(["xdg-open", out])), row.play_btn.show()
            ))
            return True
        else:
            GLib.idle_add(lambda: (row.set_active(False), row.progress.set_fraction(0.0), row.info.set_markup("<span foreground='#e74c3c' weight='bold'>✖ ERROR</span>"), row.log_btn.show()))
            return False

    def _handle_source_action(self, path):
        idx = self.after_action.get_active()
        try:
            if idx == 1: subprocess.run(["trash-put", path], check=True)
            elif idx == 2: os.remove(path)
        except Exception as e: self.send_notification("Error", f"Failed to remove source: {e}")

    def _handle_completion(self):
        self.send_notification("Conversion Complete", "All tasks finished.")
        if self.after_complete.get_active() == 1: self.start_countdown(60, "Shutdown in", lambda: subprocess.run(["systemctl", "poweroff"]))
        sec = AUTO_CLOSE_MAP.get(self.auto_close.get_active_text(), 0)
        if sec > 0: self.start_countdown(sec, "Closing in", Gtk.main_quit)

    def start_countdown(self, seconds, prefix, callback):
        self.rem_sec = seconds
        def _tick():
            if self.stop_requested: return False 
            if self.rem_sec > 0:
                self.queue_status.set_markup(f"<span size='x-large' weight='bold' foreground='#ffb74d'>{prefix} {self.rem_sec}s...</span>")
                self.rem_sec -= 1
                return True 
            callback(); return False
        self.countdown_source_id = GLib.timeout_add(1000, _tick)

    def fmt_time(self, sec): 
        m, s = divmod(int(sec), 60); h, m = divmod(m, 60)
        return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
        
    def _gather_prefs(self): 
        return {
            "codec": self.codec.get_active(), "quality": self.quality.get_active(), 
            "auto_close": self.auto_close.get_active(), "after_action": self.after_action.get_active(), 
            "after_complete": self.after_complete.get_active(), "last_folder": self.last_folder, 
            "gpu_device": self.gpu_device.get_active()
        }

    def _load_static_css(self):
        css = """
        .dim-label { opacity: 0.8; font-size: 10px; margin-bottom: 2px; font-weight: bolder; letter-spacing: 0.5px; }
        .sidebar-bg { background-color: alpha(currentColor, 0.03); border-right: 1px solid alpha(currentColor, 0.1); }
        .row-card { border-radius: 12px; border: 1px solid alpha(currentColor, 0.08); background-color: alpha(currentColor, 0.03); padding: 8px; }
        .active-row .row-card { border: 1px solid #2ec27e; background-color: alpha(#2ec27e, 0.08); }
        .thumbnail { border-radius: 8px; background-color: #000000; }
        .drag-active { border: 2px dashed #2ec27e; background-color: alpha(#2ec27e, 0.1); }
        .destructive-action { background-image: none; background-color: #e74c3c; color: white; }
        .flat-button { min-height: 24px; min-width: 24px; padding: 0px; margin: 0px; border: none; background: transparent; box-shadow: none; color: alpha(currentColor, 0.5); }
        .flat-button:hover { background-color: alpha(currentColor, 0.1); color: #2ec27e; }
        .flat-button:active { background-color: alpha(currentColor, 0.2); }
        .suggested-action { background-image: none; background-color: #2ec27e; color: #000000; font-weight: bold; border: none; border-radius: 4px; padding: 4px 8px; }
        .suggested-action label { background-color: transparent; color: inherit; }
        .suggested-action:hover { background-color: #3ad68e; }
        .suggested-action:disabled { background-color: alpha(currentColor, 0.1); color: alpha(currentColor, 0.5); }
        .row-card:hover { background-color: alpha(currentColor, 0.08); transition: background-color 0.2s ease; }
        .row-remove-btn:hover { color: #ff5555; background-color: alpha(#ff5555, 0.1); border-radius: 4px; }
        progressbar trough { min-height: 8px; border-radius: 4px; background-color: alpha(currentColor, 0.1); }
        progressbar progress { min-height: 8px; border-radius: 4px; }
        .success-bar progress { background-color: #2ec27e; }
        """
        p = Gtk.CssProvider()
        p.load_from_data(css.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), p, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

if __name__ == "__main__": check_dependencies(); VideoConverter().show_all(); Gtk.main()