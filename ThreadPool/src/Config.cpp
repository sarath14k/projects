#include "Config.h"
#include <iostream>
#include "Constants.h"
using namespace Constants;


Config::Config(const std::string& filename) {
    config = YAML::LoadFile(filename);
}

std::string Config::getServerIP() const {
    return config[SERVER][IP].as<std::string>();
}

int Config::getServerPort() const {
    return config[SERVER][PORT].as<int>();
}

int Config::getThreadCount() const {
    return config[SERVER][THREAD_COUNT].as<int>();
}

int Config::getBacklogSize() const {
    return config[SERVER][BACKLOG_SIZE].as<int>();
}

int Config::getPollTimeout() const {
    return config[SERVER][POLL_TIMEOUT_MS].as<int>();
}

int Config::getMaxEvents() const {
    return config[SERVER][MAX_EVENTS].as<int>();
}

int Config::getBufferSize() const {
    return config[SERVER][BUFFER_SIZE].as<int>();
}

std::string Config::getClientIP() const {
    return config[CLIENT][IP].as<std::string>();
}

int Config::getClientPort() const {
    return config[CLIENT][PORT].as<int>();
}
