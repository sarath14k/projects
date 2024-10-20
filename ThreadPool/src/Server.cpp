#include "Server.h"              // Include the header file for the Server class
#include "Config.h"              // Include the Config class for configuration handling
#include "Epoll.h"               // Include the Epoll class for event handling
#include <iostream>              // Include standard input/output stream library
#include <unistd.h>              // Include for UNIX standard functions (e.g., close)
#include <arpa/inet.h>          // Include for socket functions
#include <cstring>               // Include for string manipulation functions
#include "Constants.h"           // Include constant definitions
#include <thread>                // Include for multithreading
#include <atomic>                // Include for atomic variables
#include <csignal>               // Include for signal handling
#include "GlobalState.h"         // Include the header for global state management

using namespace constants;      // Use the constants namespace

void Server::start() {
    // Load the configuration from the YAML file
    Config config(CONFIG_FILE_PATH);
    int port = config.getServerPort();
    int backlog_size = config.getBacklogSize();
    int buffer_size = config.getBufferSize();
    int max_event = config.getMaxEvents();
    std::string server_ip = config.getServerIP();

    std::signal(SIGINT, signalHandler); // Register a signal handler for SIGINT (Ctrl+C)

    // Create a socket for the server
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        std::cerr << "Error creating socket." << std::endl;
        return; // Exit if socket creation fails
    }

    sockaddr_in server_addr;
    server_addr.sin_family = AF_INET; 
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);

    if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cerr << "Error binding socket." << std::endl;
        close(server_fd);
        return; // Exit if binding fails
    }

    listen(server_fd, backlog_size); // Start listening for incoming connections

    Epoll epoll(max_event);
    epoll.addFd(server_fd);

    std::cout << "Server listening on http://" << server_ip << ":" << port << std::endl;

    // Main server loop
    while (running.load()) {
        auto activeFds = epoll.waitForEvents(500); // Wait for events with a timeout

        for (int fd : activeFds) {
            if (fd == server_fd) {
                int client_fd = accept(server_fd, nullptr, nullptr);
                if (client_fd < 0) {
                    std::cerr << "Error accepting connection." << std::endl;
                    continue; // Skip to the next iteration on error
                }
                epoll.addFd(client_fd);
                std::cout << "New client " << client_fd << " connected." << std::endl;
                std::cout << "\nPress ctrl + c to quit server\n";

            } else {
                char buffer[buffer_size];
                ssize_t count = recv(fd, buffer, buffer_size - 1, 0);
                if (count <= 0) {
                    std::cerr << "Client " << fd << " disconnected." << std::endl;
                    close(fd);
                    epoll.removeFd(fd);
                } else {
                    buffer[count] = '\0'; // Null-terminate the buffer
                    std::cout << "Received: " << buffer << std::endl;

                    // Check for exit command
                    if (strcmp(buffer, "exit") == 0) {
                    std::cerr << "Client " << fd << " disconnected." << std::endl;
                        std::string clientShutdownMessage = "Thanks for connecting Client-" + std::to_string(fd);
                        send(fd, clientShutdownMessage.c_str(), clientShutdownMessage.length(), 0);
                        close(fd);
                        epoll.removeFd(fd);
                        break; // Exit the loop
                    }

                    // Otherwise, handle the message as usual
                    sendResponse(fd, std::string(buffer));
                }
            }
        }
    }

    // Notify all clients that the server is shutting down
    for (int fd : epoll.getAllFds()) {
        std::string shutdownMessage = "Server is shutting down. Closing connection.";
        send(fd, shutdownMessage.c_str(), shutdownMessage.length(), 0);
        close(fd);
    }

    close(server_fd); // Close the server socket
    std::cout << "Server has shut down." << std::endl; // Log server shutdown
}

void Server::sendResponse(int client_fd, const std::string& message) {
    if (running.load()) { // Only send if the server is still running
        std::string response = "Server: Received your message: " + message; // Prepare the response message
        ssize_t bytes_sent = send(client_fd, response.c_str(), response.length(), 0); // Send the response to the client
        if (bytes_sent < 0) {
            std::cerr << "Error sending message to client." << std::endl; // Print error if sending fails
        }
    }
}
