#include <iostream>
#include <thread>
#include <mutex>

std::mutex mtx;
int counter = 1;
const int maxCount = 10; // Change this to set the maximum count of numbers to print

void printOdd() {
    while (counter <= maxCount) {
        std::unique_lock<std::mutex> lock(mtx);
        if (counter % 2 != 0) {
            std::cout << "Odd: " << counter << std::endl;
            counter++;
        }
    }
}

void printEven() {
    while (counter <= maxCount) {
        std::unique_lock<std::mutex> lock(mtx);
        if (counter % 2 == 0) {
            std::cout << "Even: " << counter << std::endl;
            counter++;
        }
    }
}

int main() {
    std::thread t1(printOdd);
    std::thread t2(printEven);
    
    t1.join();
    t2.join();

    return 0;
}


