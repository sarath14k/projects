#include "GlobalState.h"
#include <csignal> // For signal handling

std::atomic<bool> running(true); // Define the variable here

void signalHandler(int signum) {
    running = false; // Stop the application
}
