// src/ThreadPool.cpp
#include "ThreadPool.h" // Include the header for the ThreadPool class
#include <iostream>     // For standard I/O

// Constructor initializes the thread pool with a given number of threads
ThreadPool::ThreadPool(size_t numThreads) : stop(false) {
    for (size_t i = 0; i < numThreads; ++i) {
        workers.emplace_back([this] {
            for (;;) {
                std::function<void()> task; // Variable to hold tasks
                {
                    std::unique_lock<std::mutex> lock(this->mutex); // Lock the mutex
                    this->condition.wait(lock, [this] { return this->stop || !this->tasks.empty(); }); // Wait for a task
                    if (this->stop && this->tasks.empty()) {
                        return; // Exit thread if stopping and no tasks
                    }
                    task = std::move(this->tasks.front()); // Get the next task
                    this->tasks.pop(); // Remove the task from the queue
                }
                task(); // Execute the task
            }
        });
    }
}

// Destructor joins all threads
ThreadPool::~ThreadPool() {
    {
        std::unique_lock<std::mutex> lock(mutex); // Lock the mutex
        stop = true; // Set stop flag to true
    }
    condition.notify_all(); // Notify all threads to wake up
    for (std::thread &worker : workers) {
        worker.join(); // Wait for all threads to finish
    }
}

// Function to enqueue tasks into the thread pool
template<class F>
void ThreadPool::enqueue(F&& f) {
    {
        std::unique_lock<std::mutex> lock(mutex); // Lock the mutex
        tasks.emplace(std::forward<F>(f)); // Add the task to the queue
    }
    condition.notify_one(); // Notify one waiting thread
}
