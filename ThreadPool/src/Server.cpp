#include "Server.h"
#include "Config.h"
#include "Epoll.h"
#include <iostream>
#include <unistd.h>
#include <arpa/inet.h>
#include <cstring>

void Server::start() {
    Config config("config/config.yaml");
    int port = config.getServerPort();
    int backlog_size = config.getBacklogSize();
    int buffer_size = config.getBufferSize();

    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        std::cerr << "Error creating socket." << std::endl;
        return;
    }

    sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);

    if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cerr << "Error binding socket." << std::endl;
        close(server_fd);
        return;
    }

    listen(server_fd, backlog_size);

    Epoll epoll(10);
    epoll.addFd(server_fd);

    std::cout << "Server listening on port " << port << std::endl;

    while (true) {
        auto activeFds = epoll.waitForEvents(-1);
        for (int fd : activeFds) {
            if (fd == server_fd) {
                int client_fd = accept(server_fd, nullptr, nullptr);
                if (client_fd < 0) {
                    std::cerr << "Error accepting connection." << std::endl;
                    continue;
                }
                epoll.addFd(client_fd);
                std::cout << "New client connected." << std::endl;
            } else {
                char buffer[buffer_size];
                ssize_t count = recv(fd, buffer, buffer_size - 1, 0);
                if (count <= 0) {
                    std::cerr << "Client disconnected." << std::endl;
                    close(fd);
                    epoll.removeFd(fd);
                } else {
                    buffer[count] = '\0';
                    std::cout << "Received: " << buffer << std::endl;
                }
            }
        }
    }

    close(server_fd);
}
