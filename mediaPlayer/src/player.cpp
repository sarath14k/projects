#include "player.h"

MediaPlayer::MediaPlayer() : isPlaying(false), formatContext(nullptr), codecContext(nullptr), frame(nullptr), swsContext(nullptr), rgbFrame(nullptr), rgbBuffer(nullptr) {
    window = new Fl_Window(400, 300, "FLTK Media Player");
    playButton = new Fl_Button(100, 150, 80, 40, "Play");
    stopButton = new Fl_Button(220, 150, 80, 40, "Stop");
    displayBox = new Fl_Box(20, 20, 360, 100, "No file loaded");

    playButton->callback(play_cb, this);
    stopButton->callback(stop_cb, this);

    window->end();
    window->show();
}

MediaPlayer::~MediaPlayer() {
    stopMedia(); // Ensure media is stopped before destruction
    cleanup();
}

void MediaPlayer::cleanup() {
    if (rgbFrame) {
        av_frame_free(&rgbFrame);
        rgbFrame = nullptr;
    }
    if (rgbBuffer) {
        av_free(rgbBuffer);
        rgbBuffer = nullptr;
    }
    if (codecContext) {
        avcodec_free_context(&codecContext);
        codecContext = nullptr;
    }
    if (formatContext) {
        avformat_close_input(&formatContext);
        formatContext = nullptr;
    }
    if (swsContext) {
        sws_freeContext(swsContext);
        swsContext = nullptr;
    }
}

void MediaPlayer::playMedia(const std::string& filePath) {
    // Log the current state
    std::cout << "Starting to play media: " << filePath << std::endl;

    currentFile = filePath;
    displayBox->label(filePath.c_str());

    isPlaying = true;

    // Make sure any previous thread is cleaned up
    if (decodeThread.joinable()) {
        decodeThread.join();
    }

    decodeThread = std::thread(&MediaPlayer::decodeVideo, this, filePath);
    std::cout << "Media playback started in a new thread." << std::endl;
}

void MediaPlayer::stopMedia() {
    std::cout << "Stopping media." << std::endl;
    displayBox->label("Playback stopped.");
    isPlaying = false;

    // Join the thread if it’s joinable
    if (decodeThread.joinable()) {
        decodeThread.join();
    }
}

// Update the display function with proper handling
void MediaPlayer::updateDisplay(void* data) {
    MediaPlayer* player = static_cast<MediaPlayer*>(data);
    Fl_RGB_Image* img = new Fl_RGB_Image(player->rgbFrame->data[0], player->codecContext->width, player->codecContext->height, 3);
    
    // Update the display box with the new image
    player->displayBox->image(img);
    player->displayBox->redraw();

    // Clean up the Fl_RGB_Image when done
    delete img;
}


void MediaPlayer::decodeVideo(const std::string& filePath) {
    // Open input file
    if (avformat_open_input(&formatContext, filePath.c_str(), nullptr, nullptr) < 0) {
        std::cerr << "Error: Could not open file " << filePath << std::endl;
        return;
    }

    // Find stream info
    if (avformat_find_stream_info(formatContext, nullptr) < 0) {
        std::cerr << "Could not find stream info." << std::endl;
        avformat_close_input(&formatContext); // Clean up before returning
        return;
    }

    // Find the video stream
    int videoStreamIndex = -1;
    for (unsigned int i = 0; i < formatContext->nb_streams; i++) {
        if (formatContext->streams[i]->codecpar->codec_type == AVMEDIA_TYPE_VIDEO) {
            videoStreamIndex = i;
            break;
        }
    }

    if (videoStreamIndex == -1) {
        std::cerr << "Could not find video stream." << std::endl;
        avformat_close_input(&formatContext); // Clean up before returning
        return;
    }

    // Get the codec context
    AVCodecParameters* codecPar = formatContext->streams[videoStreamIndex]->codecpar;
    const AVCodec* codec = avcodec_find_decoder(codecPar->codec_id);
    if (!codec) {
        std::cerr << "Unsupported codec!" << std::endl;
        avformat_close_input(&formatContext); // Clean up before returning
        return;
    }

    codecContext = avcodec_alloc_context3(codec);
    if (!codecContext) {
        std::cerr << "Could not allocate codec context." << std::endl;
        avformat_close_input(&formatContext); // Clean up before returning
        return;
    }

    avcodec_parameters_to_context(codecContext, codecPar);
    if (avcodec_open2(codecContext, codec, nullptr) < 0) {
        std::cerr << "Could not open codec." << std::endl;
        avcodec_free_context(&codecContext); // Clean up codec context
        avformat_close_input(&formatContext); // Clean up before returning
        return;
    }

    frame = av_frame_alloc();
    if (!frame) {
        std::cerr << "Could not allocate frame." << std::endl;
        avcodec_free_context(&codecContext); // Clean up codec context
        avformat_close_input(&formatContext); // Clean up before returning
        return;
    }
    
    // Set up the sws context for scaling
    swsContext = sws_getContext(codecContext->width, codecContext->height, codecContext->pix_fmt,
                                codecContext->width, codecContext->height, AV_PIX_FMT_RGB24,
                                SWS_BILINEAR, nullptr, nullptr, nullptr);
    
    // Allocate buffer for RGB frame
    int numBytes = av_image_get_buffer_size(AV_PIX_FMT_RGB24, codecContext->width, codecContext->height, 1);
    rgbBuffer = (uint8_t*)av_malloc(numBytes * sizeof(uint8_t));
    rgbFrame = av_frame_alloc();

    if (!rgbFrame || !rgbBuffer) {
        std::cerr << "Could not allocate RGB frame or buffer." << std::endl;
        av_frame_free(&frame); // Clean up frame
        avcodec_free_context(&codecContext); // Clean up codec context
        avformat_close_input(&formatContext); // Clean up format context
        return;
    }

    // Use av_image_fill_arrays to fill the RGB frame
    int ret = av_image_fill_arrays(rgbFrame->data, rgbFrame->linesize, rgbBuffer, AV_PIX_FMT_RGB24, codecContext->width, codecContext->height, 1);
    if (ret < 0) {
        std::cerr << "Could not fill image arrays." << std::endl;
        av_frame_free(&rgbFrame); // Clean up RGB frame
        av_free(rgbBuffer); // Clean up RGB buffer
        av_frame_free(&frame); // Clean up frame
        avcodec_free_context(&codecContext); // Clean up codec context
        avformat_close_input(&formatContext); // Clean up format context
        return;
    }

    AVPacket packet;
    while (isPlaying && av_read_frame(formatContext, &packet) >= 0) {
        if (packet.stream_index == videoStreamIndex) {
            if (avcodec_send_packet(codecContext, &packet) == 0) {
                while (avcodec_receive_frame(codecContext, frame) == 0) {
                    // Convert the frame to RGB
                    sws_scale(swsContext, frame->data, frame->linesize, 0, codecContext->height, 
                              rgbFrame->data, rgbFrame->linesize);

                    // Call Fl::awake to update the display
                    Fl::awake(updateDisplay, this); // Make sure this line is correct
                }
            }
        }
        av_packet_unref(&packet);
    }
    
    // Cleanup resources after decoding
    cleanup();
    av_frame_free(&frame);
    av_frame_free(&rgbFrame);
    av_free(rgbBuffer);
    avcodec_free_context(&codecContext);
    avformat_close_input(&formatContext);
}

void MediaPlayer::play_cb(Fl_Widget* w, void* data) {
    MediaPlayer* player = static_cast<MediaPlayer*>(data);
    const char* file = fl_file_chooser("Choose a media file", "*", NULL);

    if (file != NULL) {
        player->playMedia(file);
    }
}

void MediaPlayer::stop_cb(Fl_Widget* w, void* data) {
    MediaPlayer* player = static_cast<MediaPlayer*>(data);
    player->stopMedia();
}

