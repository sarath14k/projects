import json
from pathlib import Path

APP_NAME = "video-converter"
CONFIG_DIR = Path.home() / ".config" / APP_NAME
CONFIG_PATH = CONFIG_DIR / "config.json"
CACHE_DIR = Path.home() / ".cache" / APP_NAME
OUTPUT_DIR_NAME = "Video converter output"

# Ensure directories exist
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

VIDEO_EXTS = {
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".webm",
    ".flv",
    ".wmv",
    ".m4v",
    ".mts",
    ".m2ts",
    ".ts",
}

CODECS = {
    "HEVC (VAAPI 10-bit)": {"name": "hevc_vaapi", "fmt": "p010", "type": "vaapi"},
    "HEVC (Standard 8-bit)": {"name": "hevc_vaapi", "fmt": "nv12", "type": "vaapi"},
    "AV1 (VAAPI 10-bit)": {"name": "av1_vaapi", "fmt": "p010", "type": "vaapi"},
    "AV1 (CPU - SVT-AV1)": {"name": "libsvtav1", "fmt": "yuv420p10le", "type": "cpu"},
}

QUALITY_MAP_GPU = {
    "Best - 95% (QV-17)": 17,
    "High - 80% (QV-20)": 20,
    "Main - 65% (QV-23)": 23,
    "Lite - 45% (QV-27)": 27,
    "Tiny - 30% (QV-32)": 32,
}

BITRATE_MULTIPLIER_MAP = {17: 0.95, 20: 0.8, 23: 0.65, 27: 0.45, 32: 0.3}

QUALITY_MAP_CPU = {
    "Preset 4 (Best Size)": 4,
    "Preset 5 (Very Slow)": 5,
    "Preset 6 (Balanced)": 6,
    "Preset 7 (Faster)": 7,
    "Preset 8 (Fast)": 8,
    "Preset 9 (Very Fast)": 9,
    "Preset 10 (Super Fast)": 10,
}

AUTO_CLOSE_MAP = {"Never": 0, "30 seconds": 30, "1 minute": 60, "2 minutes": 120, "5 minutes": 300}
AFTER_ACTIONS = ("Keep source", "Move to Trash", "Delete permanently")
AFTER_COMPLETE = ("Do nothing", "Shutdown system")

class ConfigManager:
    @staticmethod
    def load():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except:
            return {}

    @staticmethod
    def save(cfg):
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            CONFIG_PATH.write_text(json.dumps(cfg, indent=2))
        except:
            pass
