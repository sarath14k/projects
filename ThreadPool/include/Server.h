#ifndef SERVER_H
#define SERVER_H

#include <string>

class Server {
public:
    void start();
    void sendResponse(int client_fd, const std::string& message);
};

#endif // SERVER_H
