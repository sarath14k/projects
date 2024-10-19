#include "Client.h"                // Include the header file for the Client class
#include "Config.h"                // Include the header file for the Config class
#include <iostream>                // Include standard input/output stream library
#include <unistd.h>                // Include Unix standard library for close()
#include <arpa/inet.h>             // Include definitions for internet operations
#include <cstring>                 // Include string manipulation functions
#include "Constants.h"             // Include a header file for constants used in the program
#include <thread>                  // Include for multithreading
#include <atomic>                  // Include for atomic variables
#include "GlobalState.h"

using namespace constants;         // Use the constants namespace for easier access to constants

void Client::start() {
    Config config(CONFIG_FILE_PATH);  // Create a Config object to read settings from a YAML file
    std::string server_ip = config.getClientIP(); // Retrieve the server IP address from the config
    int server_port = config.getClientPort();     // Retrieve the server port number from the config
    int buffer_size = config.getBufferSize();     // Retrieve the buffer size from the config

    // Create a socket for communication
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {  // Check if the socket creation failed
        std::cerr << "Error creating socket." << std::endl; // Print an error message
        return; // Exit the start function
    }

    // Define the server address structure
    sockaddr_in server_addr; // Create a sockaddr_in structure to specify the server address
    server_addr.sin_family = AF_INET; // Set the address family to IPv4
    server_addr.sin_port = htons(server_port); // Set the port number (convert to network byte order)
    inet_pton(AF_INET, server_ip.c_str(), &server_addr.sin_addr); // Convert the IP address from text to binary

    // Attempt to connect to the server
    if (connect(sock, (sockaddr*)&server_addr, sizeof(server_addr)) < 0) { // Try to connect to the server
        std::cerr << "Error connecting to server." << std::endl; // Print an error message if connection fails
        close(sock); // Close the socket
        return; // Exit the start function
    }

    // Start a thread to handle server responses
    std::thread response_thread([&sock, buffer_size]() {
        char response[buffer_size]; // Create a buffer for server responses
        while (running) {
            ssize_t bytes_received = recv(sock, response, buffer_size - 1, 0); // Receive response from server
            if (bytes_received > 0) {
                response[bytes_received] = '\0'; // Null-terminate the received string
                std::cout << "Server response: " << response << std::endl; // Display server response
            } else {
                break; // Exit if the connection is lost or an error occurs
            }
        }
    });

    char buffer[buffer_size]; // Create a buffer for message input
    while (running) {
        std::cout << "Enter message (type 'exit' to quit): ";
        std::cin.getline(buffer, buffer_size); // Get input from user
        send(sock, buffer, strlen(buffer), 0); // Send message to server
        
        if (strcmp(buffer, "exit") == 0) {
            running = false; // Signal to stop the response thread
            break; // Exit the loop if user types "exit"
        }
    }

    close(sock); // Close the socket when done
    response_thread.join(); // Wait for the response thread to finish
}
