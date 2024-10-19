// load_yaml.cpp
#include <iostream>
#include <yaml-cpp/yaml.h>

int main() {
    // Load the YAML file
    YAML::Node config = YAML::LoadFile("config.yaml");

    // Access data from the YAML file
    if (config["port"]) {
        std::cout << "Port: " << config["port"].as<int>() << std::endl;
    }

    if (config["thread_count"]) {
        std::cout << "Thread Count: " << config["thread_count"].as<int>() << std::endl;
    }

    return 0;
}
