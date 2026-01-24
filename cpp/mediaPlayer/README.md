Media Player

This project is a simple media player application built using C++, Qt for the graphical user interface, and FFmpeg for media decoding. The player supports playing audio and video files with basic controls like play, pause, and stop.
Features

    Play audio and video files (e.g., .mp4, .mp3, .avi).
    Basic controls: Play, Pause, Stop.
    File selection through a file dialog.
    Media playback using FFmpeg libraries.
    (Optional) Volume control and seek functionality.

Requirements
Dependencies

    Qt (version 5 or later)
    FFmpeg libraries:
        libavcodec
        libavformat
        libavutil
        libswscale

Installation

    Install FFmpeg libraries and Qt:

    For Arch Linux:

    bash

sudo pacman -S ffmpeg qt5-base

Clone the repository:

bash

git clone https://github.com/yourusername/mediaplayer.git
cd mediaplayer

Create a build directory and run CMake to configure the project:

bash

mkdir build
cd build
cmake ..
make

Run the media player:

bash

    ./MediaPlayer

Usage

    Launch the application.
    Click the Play button to open a file dialog and select a media file (e.g., .mp4, .mp3).
    Use the Pause and Stop buttons to control playback.

File Structure

makefile

MediaPlayer/
├── include/
│   └── player.h          # Header file for the media player class
├── src/
│   ├── main.cpp          # Entry point of the application
│   └── player.cpp        # Implementation of the media player functionality
├── ui/
│   └── mainwindow.ui     # GUI design file created with Qt Designer
├── CMakeLists.txt        # CMake configuration file
└── README.md             # Project description and instructions

Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
TODOs:

    Add volume control.
    Implement seek functionality.
    Improve error handling and support for more file formats.

License

This project is licensed under the MIT License. See the LICENSE file for details.