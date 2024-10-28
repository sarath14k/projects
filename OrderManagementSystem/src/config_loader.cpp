#include "config_loader.h"
#include <iostream>

ConfigLoader::ConfigLoader(const std::string& configFilePath) {
    try {
        config = YAML::LoadFile(configFilePath);
    } catch (const std::exception& e) {
        std::cerr << "Failed to load configuration file: " << e.what() << std::endl;
    }
}

std::string ConfigLoader::getApiKey() const {
    return config["api"]["key"].as<std::string>();
}

std::string ConfigLoader::getApiSecret() const {
    return config["api"]["secret"].as<std::string>();
}

std::string ConfigLoader::getBaseUrl() const {
    return config["api"]["base_url"].as<std::string>();
}

double ConfigLoader::getOrderAmount() const {
    return config["settings"]["order_amount"].as<double>();
}

double ConfigLoader::getDefaultPrice() const {
    return config["settings"]["default_price"].as<double>();
}

std::vector<std::string> ConfigLoader::getSymbols() const {
    std::vector<std::string> symbols;
    for (const auto& symbol : config["settings"]["symbols"]) {
        symbols.push_back(symbol.as<std::string>());
    }
    return symbols;
}
