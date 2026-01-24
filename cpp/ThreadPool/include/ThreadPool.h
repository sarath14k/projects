// include/ThreadPool.h
#ifndef THREADPOOL_H
#define THREADPOOL_H

#include <vector>
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <functional>

class ThreadPool {
public:
    ThreadPool(size_t numThreads); // Constructor to initialize thread pool
    ~ThreadPool(); // Destructor to join all threads

    template<class F>
    void enqueue(F&& f); // Function to add tasks to the thread pool

private:
    std::vector<std::thread> workers; // Vector to hold worker threads
    std::queue<std::function<void()>> tasks; // Queue to hold tasks
    std::mutex mutex; // Mutex for synchronizing access to tasks
    std::condition_variable condition; // Condition variable for task notification
    bool stop; // Flag to indicate if the pool is stopping
};

#endif // THREADPOOL_H
