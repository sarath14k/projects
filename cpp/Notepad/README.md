# Notepad

A simple text editor built using Qt5/Qt6 and C++. This application provides a basic GUI for creating, editing, and saving text files.

## Features

- Create new text files
- Open existing text files
- Edit and save text content
- Basic formatting options (if implemented)
- User-friendly interface

## Requirements

- **Qt5 or Qt6**: Make sure you have the Qt development libraries installed on your system.
- **C++17**: The project is built using C++17 standard.

## Installation

### Prerequisites

Make sure you have the necessary packages installed. On Ubuntu or Zorin OS, you can use:

```bash
sudo apt update
sudo apt install qt5-default qtbase5-dev qttools5-dev qttools5-dev-tools

## Build the project
mkdir build
cd build
cmake ..
make
./Notepad

