# MeetShare Pro 🚀

High-performance media sharing for Google Meet on Linux (PikaOS/Hyprland). Bypasses screen-sharing limitations with native MPV integration and PipeWire audio routing.

---

## 🎧 Features
- **Pro Audio Matrix**: Simultaneous routing of your voice + video audio + meeting audio.
- **High Quality**: Uses native `mpv` with PipeWire instead of browser-based sharing.
- **Dual Monitoring**: Hear the video in your headset while sharing it with the meeting.
- **Automated**: Auto-links ports every time you play a video.

---

## 🚀 Daily Usage
You don't need to run any terminal commands! 

1.  Open Chrome and click the **MeetShare Extension** icon.
2.  Click **Open Player Tab** (or go directly to `http://127.0.0.1:9999/`).
3.  Click **Open Video in MPV** and select your movie.
4.  In Google Meet, share the **MPV Window** (`MeetShare_MPV`).
5.  **Important**: Turn **OFF** "Noise Cancellation" in Google Meet settings for best audio.

---

## 🛠 Fresh Installation (New OS)
If you ever reinstall your OS, follow these simple steps:

1.  **Clone this repo**:
    ```bash
    git clone git@github.com:sarath14k/projects.git
    cd ~/projects/pikaHyprland
    ```
2.  **Run the Installer**:
    ```bash
    chmod +x install.sh
    ./install.sh
    ```
3.  **Setup the Browser Extension**:
    - Go to `chrome://extensions`
    - Enable **Developer Mode**.
    - Click **Load unpacked** and select the `meet_extension` folder inside this directory.

---

## 📂 Project Structure
- `mpv_bridge.py`: The Python backend (Bridge).
- `index.html`: The Mission Control Dashboard.
- `meet_extension/`: The Chrome extension files.
- `install.sh`: One-click system setup script.

---
*Created with ❤️ for a seamless Linux sharing experience.*
