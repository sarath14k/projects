// src/Server.cpp
#include "Server.h"         // Include the header file for the Server class
#include <iostream>         // Include iostream for input and output
#include <netinet/in.h>     // Include netinet/in.h for network-related definitions
#include <unistd.h>         // Include unistd.h for close() function
#include <cstring>          // Include cstring for memory manipulation functions
#include <stdexcept>        // Include stdexcept for exception handling
#include "Constants.h"
// Constructor to initialize the server with the given port and thread count
Server::Server(int port, int threadCount) 
    : port(port), running(false), threadCount(threadCount) {} // Initialize member variables


// Method to start the server
void Server::start() {
    running = true; // Set the running flag to true
    int serverSocket = socket(AF_INET, SOCK_STREAM, 0); // Create a socket for the server

    if (serverSocket < 0) { // Check for socket creation error
        throw std::runtime_error("Failed to create socket"); // Throw an exception if socket creation fails
    }

    sockaddr_in serverAddr{}; // Create a sockaddr_in structure to hold server address
    serverAddr.sin_family = AF_INET; // Set address family to IPv4
    serverAddr.sin_addr.s_addr = INADDR_ANY; // Accept connections from any address
    serverAddr.sin_port = htons(port); // Convert port number to network byte order

    // Bind the socket to the address and check for errors
    if (bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
        close(serverSocket); // Close the socket if binding fails
        throw std::runtime_error("Failed to bind socket"); // Throw an exception for binding failure
    }

    // Listen for incoming connections with a backlog of 5
    if (listen(serverSocket, 5) < 0) {
        close(serverSocket); // Close the socket if listening fails
        throw std::runtime_error("Failed to listen on socket"); // Throw an exception for listening failure
    }

    std::cout << "Server listening on " << "http://localhost:" << port << std::endl; // Output to indicate server is running

    // Main loop to accept and handle client connections
    while (running) {
        int clientSocket = accept(serverSocket, nullptr, nullptr); // Accept a new client connection

        if (clientSocket < 0) { // Check for errors in accepting a connection
            if (running) { // Only output if server is still running
                std::cerr << "Failed to accept client connection" << std::endl; // Output error message
            }
            continue; // Skip to the next iteration if accepting fails
        }

        threads.emplace_back(&Server::handleClient, this, clientSocket); // Start a new thread to handle the client
    }

    close(serverSocket); // Close the server socket when stopping
}

// Method to stop the server
void Server::stop() {
    running = false; // Set the running flag to false
    // Join all threads to ensure they finish before stopping the server
    for (auto& thread : threads) {
        if (thread.joinable()) { // Check if the thread is joinable
            thread.join(); // Wait for the thread to finish execution
        }
    }
}

// Method to handle individual client connections
void Server::handleClient(int clientSocket) {
    char buffer[1024] = {0}; // Buffer to hold the incoming data from the client
    ssize_t bytesRead = read(clientSocket, buffer, sizeof(buffer)); // Read data from the client socket

    if (bytesRead < 0) { // Check for read errors
        std::cerr << "Error reading from client socket" << std::endl; // Output error message
    } else {
        // Create a simple HTTP response
        std::string response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hello from Multi-threaded Web Server!</h1>";
        respond(clientSocket, response); // Send the response back to the client
    }
    
    close(clientSocket); // Close the client socket after responding
}

// Method to send a response to the client
void Server::respond(int clientSocket, const std::string& response) {
    ssize_t bytesSent = send(clientSocket, response.c_str(), response.size(), 0); // Send the response over the client socket
    if (bytesSent < 0) { // Check for send errors
        std::cerr << "Error sending response to client" << std::endl; // Output error message
    }
}
