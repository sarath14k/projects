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

MEDIA_EXTS = {
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
    ".mp3",
    ".m4a",
    ".aac",
    ".flac",
    ".opus",
    ".wav",
    ".ogg",
}

CODECS = {
    "AV1 (VAAPI 10-bit)": {"name": "av1_vaapi", "fmt": "p010", "type": "vaapi"},
    "HEVC (VAAPI 10-bit)": {"name": "hevc_vaapi", "fmt": "p010", "type": "vaapi"},
    "HEVC (Standard 8-bit)": {"name": "hevc_vaapi", "fmt": "nv12", "type": "vaapi"},
    "AV1 (CPU - SVT-AV1)": {"name": "libsvtav1", "fmt": "yuv420p10le", "type": "cpu"},
}

QUALITY_MAP_GPU = {
    "Best - 95%": "best",
    "High - 80%": "high",
    "Main - 65%": "main",
    "Lite - 45%": "lite",
    "Tiny - 30%": "tiny",
}

GPU_BITRATE_TARGETS = {
    "best": 1.0,
    "high": 0.8,
    "main": 0.65,
    "lite": 0.45,
    "tiny": 0.3,
}

GPU_QV_MAP_AV1 = {
    "best": 20,
    "high": 23,
    "main": 26,
    "lite": 30,
    "tiny": 34,
}

GPU_QV_MAP_HEVC = {
    "best": 15,
    "high": 18,
    "main": 21,
    "lite": 25,
    "tiny": 29,
}

DEFAULT_COMPRESSION_LEVEL = 1

QUALITY_MAP_CPU = {
    "Preset 4 (Best)": 4,
    "Preset 5 (High)": 5,
    "Preset 6 (Lite)": 6,
    "Preset 7 (Tiny)": 7,
    "Preset 8 (Fast)": 8,
    "Preset 9 (quick)": 9,
    "Preset 10 (Instant)": 10,
}

AUDIO_CODECS = {
    "Copy": "copy",
    "AAC (Web Recommended)": "aac",
    "MP3": "libmp3lame",
    "Opus": "libopus",
    "FLAC": "flac",
}

PROCESS_MODES = ("Video + Audio", "Audio Only")

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
