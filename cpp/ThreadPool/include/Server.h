// src/Server.h
#ifndef SERVER_H
#define SERVER_H

#include <vector>
#include <thread>

class Server {
public:
    // Updated constructor to take port and thread count
    Server(int port, int threadCount); 

    void start();   // Start the server
    void stop();    // Stop the server

private:
    int port;                   // Port number for the server
    bool running;               // Flag to check if the server is running
    int threadCount;            // Number of threads for handling clients
    std::vector<std::thread> threads; // Vector to hold threads
    void handleClient(int clientSocket); // Method to handle client connections
    void respond(int clientSocket, const std::string& response); // Method to send responses
};

#endif // SERVER_H
