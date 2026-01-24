#ifndef CONSTANT_H
#define CONSTANT_H
#include <string>

namespace Constants {
    const std::string CONFIG_FILE_PATH = "config/config.yaml"; // Path to the configuration file
    const std::string SERVER = "server";
    const std::string CLIENT = "client";
    const std::string IP = "ip";
    const std::string PORT = "port";
    const std::string THREAD_COUNT = "thread_count"; // Added for thread count
    const std::string BACKLOG_SIZE = "backlog_size";
    const std::string POLL_TIMEOUT_MS = "poll_timeout_ms";
    const std::string MAX_EVENTS = "max_events";
    const std::string BUFFER_SIZE = "buffer_size";
}

#endif // CONSTANT_H
