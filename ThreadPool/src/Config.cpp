#include "Config.h"
#include <yaml-cpp/yaml.h> // Include the yaml-cpp header

bool Config::load(const std::string& filename) {
    YAML::Node config = YAML::LoadFile(filename); // Load YAML file

    // Directly access the server node values
    port = config["server"]["port"].as<int>();
    threadCount = config["server"]["thread_count"].as<int>();

    return true; // Return true if loading was successful
}

int Config::getPort() const {
    return port; // Return the port number
}

int Config::getThreadCount() const {
    return threadCount; // Return the thread count
}
