import json
from pathlib import Path
from ..config import *

class PrefsManager:
    def __init__(self, window):
        self.window = window
        self.config = {}

    def load_prefs(self):
        try:
            if CONFIG_PATH.exists():
                with open(CONFIG_PATH, "r") as f:
                    self.config = json.load(f)
        except Exception as e:
            print(f"Failed to load config: {e}")

    def save_prefs(self):
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            prefs = self.gather_prefs()
            with open(CONFIG_PATH, "w") as f:
                json.dump(prefs, f, indent=4)
        except Exception as e:
            print(f"Failed to save config: {e}")

    def restore_ui_state(self):
        if not self.config:
            return

        # Restore combos
        try:
            if "codec" in self.config:
                self.window.codec.set_active(self.config["codec"])
            if "quality" in self.config:
                self.window.quality.set_active(self.config["quality"])
            if "auto_close" in self.config:
                self.window.auto_close.set_active(self.config["auto_close"])
            if "after_action" in self.config:
                self.window.after_action.set_active(self.config["after_action"])
            if "after_complete" in self.config:
                self.window.after_complete.set_active(self.config["after_complete"])
            if "gpu_device" in self.config:
                self.window.gpu_device.set_active(self.config["gpu_device"])
            if "compression_level" in self.config:
                self.window.compression_level.set_active(self.config["compression_level"])
        except:
            pass

        # Restore path
        self.window.last_folder = self.config.get("last_folder", str(Path.home()))

        # Restore Theme
        pitch_black = False
        if "pitch_black" in self.config:
            pitch_black = self.config.get("pitch_black")
        elif "theme_mode" in self.config:
            if self.config.get("theme_mode") == "pitch-black":
                pitch_black = True

        self.window.theme_switch.set_active(pitch_black)
        # Apply manually
        self.window.on_theme_toggled(self.window.theme_switch, pitch_black)

    def gather_prefs(self):
        return {
            "codec": self.window.codec.get_active(),
            "quality": self.window.quality.get_active(),
            "auto_close": self.window.auto_close.get_active(),
            "after_action": self.window.after_action.get_active(),
            "after_complete": self.window.after_complete.get_active(),
            "last_folder": self.window.last_folder,
            "gpu_device": self.window.gpu_device.get_active(),
            "compression_level": self.window.compression_level.get_active(),
            "pitch_black": self.window.theme_switch.get_active(),
        }
