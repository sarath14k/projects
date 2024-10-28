#ifndef CONFIG_LOADER_H
#define CONFIG_LOADER_H

#include <string>
#include <yaml-cpp/yaml.h>

class ConfigLoader {
public:
    ConfigLoader(const std::string& configFilePath);
    std::string getApiKey() const;
    std::string getApiSecret() const;
    std::string getBaseUrl() const;
    double getOrderAmount() const;
    double getDefaultPrice() const;
    std::vector<std::string> getSymbols() const;

private:
    YAML::Node config;
};

#endif
