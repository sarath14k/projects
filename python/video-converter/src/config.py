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
    "Best - 90% (QV-18)": 18,
    "High - 70% (QV-22)": 22,
    "Main - 50% (QV-26)": 26,
    "Lite - 30% (QV-30)": 30,
    "Tiny - 20% (QV-34)": 34,
}

BITRATE_MULTIPLIER_MAP = {18: 0.9, 22: 0.7, 26: 0.5, 30: 0.3, 34: 0.2}

QUALITY_MAP_CPU = {
    "Preset 4 (Best Size)": 4,
    "Preset 5 (Very Slow)": 5,
    "Preset 6 (Balanced)": 6,
    "Preset 7 (Faster)": 7,
    "Preset 8 (Fast)": 8,
    "Preset 9 (Very Fast)": 9,
    "Preset 10 (Super Fast)": 10,
}

AUTO_CLOSE_MAP = {"Never": 0, "After 1 min": 60, "After 5 min": 300}
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
