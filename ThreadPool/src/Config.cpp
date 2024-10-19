#include "Config.h"
#include <iostream>

Config::Config(const std::string& filename) {
    config = YAML::LoadFile(filename);
}

std::string Config::getServerIP() const {
    return config["server"]["ip"].as<std::string>();
}

int Config::getServerPort() const {
    return config["server"]["port"].as<int>();
}

int Config::getThreadCount() const {
    return config["server"]["thread_count"].as<int>();
}

int Config::getBacklogSize() const {
    return config["server"]["backlog_size"].as<int>();
}

int Config::getPollTimeout() const {
    return config["server"]["poll_timeout_ms"].as<int>();
}

int Config::getMaxEvents() const {
    return config["server"]["max_events"].as<int>();
}

int Config::getBufferSize() const {
    return config["server"]["buffer_size"].as<int>();
}

std::string Config::getClientIP() const {
    return config["client"]["server_ip"].as<std::string>();
}

int Config::getClientPort() const {
    return config["client"]["server_port"].as<int>();
}
