#ifndef EPOLL_H
#define EPOLL_H

#include <sys/epoll.h>
#include <vector>
#include <functional>

class Epoll {
public:
    Epoll(int maxEvents);
    ~Epoll();
    
    void addFd(int fd);
    void removeFd(int fd);
    std::vector<int> waitForEvents(int timeout);

private:
    int epollFd;
    std::vector<struct epoll_event> events;
};

#endif // EPOLL_H
