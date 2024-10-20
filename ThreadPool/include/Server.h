#ifndef SERVER_H
#define SERVER_H

#include <string> // Include string header

class Server {
public:
    void start(); // Start the server
    void sendResponse(int client_fd, const std::string& message); // Send a response to a client
};

#endif // SERVER_H
