#ifndef PLAYER_H
#define PLAYER_H

#include <FL/Fl.H>
#include <FL/Fl_Window.H>
#include <FL/Fl_Box.H>
#include <FL/Fl_Button.H>
#include <string>
#include <thread>
#include <atomic>

#include <FL/Fl_File_Chooser.H>
#include <FL/Fl_Image.H>
#include <FL/Fl_RGB_Image.H>
#include <iostream>

extern "C" {
#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>
#include <libswscale/swscale.h>
#include <libavutil/imgutils.h>
}

class MediaPlayer {
public:
    MediaPlayer();
    ~MediaPlayer();

    void playMedia(const std::string& filePath);
    void stopMedia();

private:
    static void play_cb(Fl_Widget* w, void* data);
    static void stop_cb(Fl_Widget* w, void* data);
    static void updateDisplay(void* data); // <-- Declare as static

    void decodeVideo(const std::string& filePath);
    void cleanup();

    Fl_Window* window;
    Fl_Box* displayBox;
    Fl_Button* playButton;
    Fl_Button* stopButton;

    std::thread decodeThread;
    std::atomic<bool> isPlaying;
    AVFormatContext* formatContext;
    AVCodecContext* codecContext;
    AVFrame* frame;
    SwsContext* swsContext;
    AVFrame* rgbFrame;
    uint8_t* rgbBuffer;
    std::string currentFile;
};

#endif // PLAYER_H
