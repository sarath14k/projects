#include "Config.h"
#include "Server.h"
#include "Constants.h"

int main() {
    Config config; // Create a Config object
    // Load configuration from the YAML file and check if it was successful
    if (!config.load(Constants::CONFIG_FILE_PATH)) {
        return 1; // Exit if configuration loading failed
    }
    
    int port = config.getPort(); // Get port
    int threadCount = config.getThreadCount(); // Get thread count
    // Create a Server object with the port and thread count from configuration
    Server server(port, threadCount);
    server.start(); // Start the server to listen for incoming connections

    return 0; // Exit the program
}
