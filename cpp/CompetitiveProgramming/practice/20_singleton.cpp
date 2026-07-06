#include <iostream>
#include <string>
using namespace std;

/*
 * ============================================================================
 * DESIGN PATTERN: THREAD-SAFE SINGLETON (MEYERS' IMPLEMENTATION)
 * ============================================================================
 * PURPOSE:
 * Guarantees that only ONE instance of a class exists, even when accessed 
 * by multiple execution threads concurrently, without requiring verbose or 
 * slow manual mutex locks.
 *
 * KEY STRUCTURAL POINTS:
 * 1. Static Local Variable: Thread-safety is built-in by core C++11 rules. The 
 *    compiler automatically injects locks around static local initialization.
 * 2. Delete Keywords: Expressly breaks copying mechanics so threads can't clone it.
 * ============================================================================
 */

class ThreadSafeLogger {
private:
    // POINT 1: Private constructor prevents any thread from calling 'new' directly.
    ThreadSafeLogger() { 
        cout << "Logger Safely Initialized Once Across All Threads.\n"; 
    }

public:
    // POINT 2: Delete copy constructor and assignment operator to prevent cloning.
    ThreadSafeLogger(const ThreadSafeLogger&) = delete;
    ThreadSafeLogger& operator=(const ThreadSafeLogger&) = delete;

    // POINT 1: Static function returning a reference to the single instance.
    static ThreadSafeLogger& getInstance() {
        // C++11 standard mandates this initialization is thread-safe!
        // If thread B calls this while thread A is constructing it, thread B 
        // will safely pause and wait until construction finishes.
        static ThreadSafeLogger instance; 
        return instance;
    }

    void logMessage(const string& msg) {
        cout << "[Log]: " << msg << "\n";
    }
};

int main() {
    // No matter which thread running concurrently executes this line, 
    // they all get safely routed to the exact same memory instance.
    ThreadSafeLogger::getInstance().logMessage("Application started successfully.");
    ThreadSafeLogger::getInstance().logMessage("Processing transaction data...");
    
    return 0;
}
