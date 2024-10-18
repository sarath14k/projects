#ifndef CONFIG_H
#define CONFIG_H

#include "Constants.h"
#include <string>
#include <yaml-cpp/yaml.h>

class Config {
public:
    bool load(const std::string& filename); // Load configuration from a file
    int getPort() const;                     // Get the port number
    int getThreadCount() const;              // Get the thread count
private:
    int port;           // Port number
    int threadCount;    // Number of threads
};

#endif // CONFIG_H
