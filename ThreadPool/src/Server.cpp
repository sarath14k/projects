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
#include "GlobalState.h"       // Assuming you have a header for global state management

using namespace constants;      // Use the constants namespace

void signalHandler(int signum) {
    std::cout << "Shutting down server..." << std::endl;
    running = false; // Set running to false to exit the loop
}

void Server::start() { // Method to start the server
    Config config(CONFIG_FILE_PATH); // Load the configuration from the YAML file
    int port = config.getServerPort(); // Get the server port from configuration
    int backlog_size = config.getBacklogSize(); // Get the backlog size for listen()
    int buffer_size = config.getBufferSize(); // Get the buffer size for receiving messages
    int max_event = config.getMaxEvents();
    std::string server_ip = config.getServerIP();

    // Register signal handler for SIGINT (Ctrl+C)
    std::signal(SIGINT, signalHandler);

    int server_fd = socket(AF_INET, SOCK_STREAM, 0); // Create a socket for the server
    if (server_fd < 0) { // Check for errors in socket creation
        std::cerr << "Error creating socket." << std::endl;
        return; // Exit if socket creation fails
    }

    sockaddr_in server_addr; // Create a sockaddr_in structure for the server address
    server_addr.sin_family = AF_INET; // Set address family to IPv4
    server_addr.sin_addr.s_addr = INADDR_ANY; // Accept connections from any IP address
    server_addr.sin_port = htons(port); // Set the port number, converting to network byte order

    if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cerr << "Error binding socket. Error code: " << errno << std::endl;
        perror("Bind failed");  // This will give you a more descriptive error message
        close(server_fd);
        return;
    }

    listen(server_fd, backlog_size); // Start listening for incoming connections with a specified backlog size

    Epoll epoll(max_event); // Create an Epoll instance with a maximum events
    epoll.addFd(server_fd); // Add the server socket file descriptor to the epoll instance

    std::cout << "Server listening on http://" << server_ip << ":" << port << std::endl; // Log the server status

    // Thread to handle server shutdown on input
    std::thread input_thread([]() {
        std::string command;
        while (running) {
            std::getline(std::cin, command);
            if (command == "exit" || command == "quit") {
                running = false; // Stop the server
                std::cout << "Shutting down the server..." << std::endl;
            }
        }
    });

    while (running) { // Main server loop
        auto activeFds = epoll.waitForEvents(-1); // Wait indefinitely for events
        for (int fd : activeFds) { // Iterate over active file descriptors
            if (fd == server_fd) { // Check if the active fd is the server socket
                int client_fd = accept(server_fd, nullptr, nullptr); // Accept a new client connection
                if (client_fd < 0) { // Check for errors in accepting a connection
                    std::cerr << "Error accepting connection." << std::endl;
                    continue; // Skip to the next iteration on error
                }
                epoll.addFd(client_fd); // Add the client socket to the epoll instance
                std::cout << "New client " << client_fd << " connected." << std::endl; // Log the new client connection
            } else { // Otherwise, handle incoming data from a connected client
                char buffer[buffer_size]; // Create a buffer for incoming messages
                ssize_t count = recv(fd, buffer, buffer_size - 1, 0); // Receive data from the client
                if (count <= 0) { // Check if the client has disconnected or an error occurred
                    std::cerr << "Client " << fd << " disconnected." << std::endl;
                    close(fd); // Close the client socket
                    epoll.removeFd(fd); // Remove the client socket from the epoll instance
                } else { // Data was received successfully
                    buffer[count] = '\0'; // Null-terminate the buffer to make it a valid string
                    std::cout << "Received: " << buffer << std::endl; // Log the received message
                    sendResponse(fd, std::string(buffer));                
                }
            }
        }
    }

    close(server_fd); // Close the server socket
    input_thread.join(); // Wait for the input thread to finish
}

void Server::sendResponse(int client_fd, const std::string& message) {
    std::string response = "Server: Received your message: " + message;
    ssize_t bytes_sent = send(client_fd, response.c_str(), response.length(), 0);
    if (bytes_sent < 0) {
        std::cerr << "Error sending response to the client: " << client_fd << std::endl;
    }
}
