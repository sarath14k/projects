#ifndef GLOBALSTATE_H
#define GLOBALSTATE_H

#include <atomic>

extern std::atomic<bool> running; // Declare running as extern

void signalHandler(int signum); // Declare the signal handler function

#endif // GLOBALSTATE_H
