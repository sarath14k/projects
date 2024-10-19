#ifndef CONFIG_H
#define CONFIG_H

#include <string>
#include <yaml-cpp/yaml.h>

class Config {
public:
    Config(const std::string& filename);
    
    std::string getServerIP() const;
    int getServerPort() const;
    int getThreadCount() const;
    int getBacklogSize() const;
    int getPollTimeout() const;
    int getMaxEvents() const;
    int getBufferSize() const;

    std::string getClientIP() const;
    int getClientPort() const;

private:
    YAML::Node config;
};

#endif // CONFIG_H
