#include "Epoll.h"               // Include the header file for the Epoll class
#include <stdexcept>             // Include for standard exception handling
#include <iostream>              // Include standard input/output stream library
#include <unistd.h>              // Include for the close function

Epoll::Epoll(int maxEvents) : events(maxEvents) { // Constructor with maxEvents as parameter
    epollFd = epoll_create1(0); // Create an epoll instance with no special flags
    if (epollFd < 0) {           // Check if the epoll instance creation failed
        throw std::runtime_error("Error creating epoll instance."); // Throw an exception if it failed
    }
}

Epoll::~Epoll() { // Destructor
    close(epollFd); // Close the epoll file descriptor to free resources
}

void Epoll::addFd(int fd) { // Method to add a file descriptor to the epoll instance
    struct epoll_event event; // Create an epoll_event structure
    event.events = EPOLLIN;   // Set the event to monitor for incoming data
    event.data.fd = fd;       // Associate the file descriptor with the event

    // Add the file descriptor to the epoll instance
    if (epoll_ctl(epollFd, EPOLL_CTL_ADD, fd, &event) < 0) {
        std::cerr << "Error adding file descriptor to epoll." << std::endl; // Print error if adding fails
    } else {
        fds[fd] = fd; // Track the added file descriptor
    }
}

void Epoll::removeFd(int fd) { // Method to remove a file descriptor from the epoll instance
    epoll_ctl(epollFd, EPOLL_CTL_DEL, fd, nullptr); // Remove the file descriptor
    fds.erase(fd); // Remove from the tracking map
}

std::vector<int> Epoll::waitForEvents(int timeout) { // Method to wait for events on monitored file descriptors
    int n = epoll_wait(epollFd, events.data(), events.size(), timeout); // Wait for events with a specified timeout
    std::vector<int> activeFds; // Vector to store active file descriptors

    for (int i = 0; i < n; i++) { // Loop through the number of events returned
        activeFds.push_back(events[i].data.fd); // Add each active file descriptor to the vector
    }

    return activeFds; // Return the vector of active file descriptors
}

// New function to get all tracked file descriptors
std::vector<int> Epoll::getAllFds() {
    std::vector<int> allFds;
    for (const auto& pair : fds) {
        allFds.push_back(pair.first); // Add each tracked fd to the vector
    }
    return allFds; // Return the vector of all fds
}
