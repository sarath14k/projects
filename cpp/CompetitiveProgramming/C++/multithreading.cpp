#include <iostream>
#include <thread>
#include <chrono> // For std::chrono::seconds
#include <mutex>  // For std::mutex

using namespace std;

mutex mtx; // Mutex to lock `std::cout` access

void makeToast()
{
    {
        lock_guard<mutex> lock(mtx);
        cout << "Started Making Toast" << endl;
    }
    std::this_thread::sleep_for(std::chrono::seconds(2)); // Simulate time to make toast
    {
        lock_guard<mutex> lock(mtx);
        cout << "Prepared Toast" << endl;
    }
}

void makeJuice()
{
    {
        lock_guard<mutex> lock(mtx);
        cout << "Started Making Juice" << endl;
    }
    std::this_thread::sleep_for(std::chrono::seconds(2)); // Simulate time to make juice
    {
        lock_guard<mutex> lock(mtx);
        cout << "Prepared Juice" << endl;
    }
}

void boilEgg()
{
    {
        lock_guard<mutex> lock(mtx);
        cout << "Started Boiling Egg" << endl;
    }
    std::this_thread::sleep_for(std::chrono::seconds(2)); // Simulate time to boil egg
    {
        lock_guard<mutex> lock(mtx);
        cout << "Prepared Egg" << endl;
    }
}

int main()
{
    // Create threads for making toast, juice, and boiling egg
    thread t1(makeToast);
    thread t2(makeJuice);
    thread t3(boilEgg);

    // Wait for all threads to finish
    t1.join();
    t2.join();
    t3.join();

    return 0;
}

/*
Mutex: std::mutex mtx; is used to protect shared access to std::cout.
lock_guard: I wrapped std::cout operations inside a lock_guard<mutex> block,
which locks the mutex while printing to ensure that only one thread at a time accesses the output stream.

The lock_guard automatically locks the mutex when entering the block and unlocks it when the block is
exited (when it goes out of scope). This prevents the output from being interleaved or jumbled,
ensuring that each message is printed atomically.

we are using std::lock_guard to handle the locking and unlocking of the mutex. 
The lock_guard automatically acquires the lock when it is created and releases the lock when 
it goes out of scope (i.e., when the block is exited).

So, you don't need to explicitly release the lock because lock_guard handles it for you.

*/

/*
If you want more control (e.g., manually unlocking the mutex before the block ends or locking it 
conditionally), you can use std::unique_lock


*/

#include <iostream>
#include <thread>
#include <chrono> // For std::chrono::seconds
#include <mutex>  // For std::mutex

using namespace std;

mutex mtx; // Mutex to lock `std::cout`

void makeToast()
{
    {
        unique_lock<mutex> lock(mtx);
        cout << "Started Making Toast" << endl;
        lock.unlock(); // Manually unlock here if you want
    }
    std::this_thread::sleep_for(std::chrono::seconds(2)); // Simulate time to make toast
    {
        unique_lock<mutex> lock(mtx);
        cout << "Prepared Toast" << endl;
    }
}

void makeJuice()
{
    {
        unique_lock<mutex> lock(mtx);
        cout << "Started Making Juice" << endl;
        lock.unlock(); // Manually unlock here if you want
    }
    std::this_thread::sleep_for(std::chrono::seconds(2)); // Simulate time to make juice
    {
        unique_lock<mutex> lock(mtx);
        cout << "Prepared Juice" << endl;
    }
}

void boilEgg()
{
    {
        unique_lock<mutex> lock(mtx);
        cout << "Started Boiling Egg" << endl;
        lock.unlock(); // Manually unlock here if you want
    }
    std::this_thread::sleep_for(std::chrono::seconds(2)); // Simulate time to boil egg
    {
        unique_lock<mutex> lock(mtx);
        cout << "Prepared Egg" << endl;
    }
}

int main()
{
    // Create threads for making toast, juice, and boiling egg
    thread t1(makeToast);
    thread t2(makeJuice);
    thread t3(boilEgg);

    // Wait for all threads to finish
    t1.join();
    t2.join();
    t3.join();

    return 0;
}

std::lock_guard is a simpler, safer way to lock and unlock a mutex, and you don't need to worry about  
explicitly releasing the lock—it automatically unlocks when the lock_guard goes out of scope.

std::unique_lock gives you more flexibility if you need to manually unlock or perform other operations,
but it isn't necessary in most situations.

    Automatic Unlocking : 
    In the second segment,you don’t explicitly unlock the mutex because unique_lock automatically 
    releases the lock when the block is exited.This is generally a safe and preferred approach as it 
    prevents errors,such as forgetting to unlock the mutex or unlocking it prematurely.


    In the second segment, there’s no sleeping or other time-consuming operations after printing 
    "Prepared Egg", so there’s no reason to unlock manually. The lock is only held for a short time 
    while printing, and it gets released immediately after.


First Segment (unlock manually): You unlock the mutex because you don’t need to hold it while the thread 
is sleeping for 2 seconds.

Second Segment (no manual unlock): You don’t need to manually unlock because the unique_lock will 
automatically unlock when the scope ends, and no sleeping follows.