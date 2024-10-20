#ifndef EPOLL_H
#define EPOLL_H

#include <vector>
#include <sys/epoll.h>
#include <unordered_map>

class Epoll {
public:
    Epoll(int maxEvents);                     // Constructor
    ~Epoll();                                 // Destructor
    void addFd(int fd);                       // Add file descriptor to epoll
    void removeFd(int fd);                    // Remove file descriptor from epoll
    std::vector<int> waitForEvents(int timeout); // Wait for events
    std::vector<int> getAllFds();             // Get all tracked file descriptors

private:
    int epollFd;                              // File descriptor for the epoll instance
    std::vector<struct epoll_event> events;  // Vector for storing events
    std::unordered_map<int, int> fds;        // Map to track added file descriptors
};

#endif // EPOLL_H
