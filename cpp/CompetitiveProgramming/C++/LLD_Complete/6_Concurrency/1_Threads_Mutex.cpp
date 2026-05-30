// To compile and run: cd /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/6_Concurrency && g++ -std=c++17 -pthread 1_Threads_Mutex.cpp -o 1_Threads_Mutex && ./1_Threads_Mutex
#include <iostream>
#include <thread>
#include <mutex>

/*
 * CONCEPT: Multithreading & Mutex
 * 
 * WHAT: Running multiple threads of execution concurrently to utilize multi-core processors. 
 *       Mutex (Mutual Exclusion) ensures that multiple threads do not modify shared data simultaneously.
 * 
 * HOW: Use `std::thread` to spawn threads. Use `std::mutex` and `std::lock_guard` to lock critical sections.
 * 
 * WHY: Threads improve performance via parallelism. Mutexes prevent "race conditions" where thread A 
 *      and thread B try to overwrite the same memory address at the exact same time, causing corruption.
 */

std::mutex mtx;
int counter = 0;

void incrementCounter(int id) {
    // lock_guard automatically locks the mutex, and unlocks it when it goes out of scope (RAII)
    std::lock_guard<std::mutex> lock(mtx);
    
    counter++;
    std::cout << "Thread " << id << " incremented counter to " << counter << "\n";
}

int main() {
    // Spawn two threads executing the same function
    std::thread t1(incrementCounter, 1);
    std::thread t2(incrementCounter, 2);
    
    // Wait for threads to finish before main exits
    t1.join();
    t2.join();
    
    std::cout << "Final Counter: " << counter << "\n";
    return 0;
}
