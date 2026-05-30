// To compile and run: cd
// /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/3_DesignPatterns
// && g++ -std=c++17 1_Singleton.cpp -o 1_Singleton && ./1_Singleton
#include <iostream>

/*
 * CONCEPT: Singleton Design Pattern (Thread-Safe Meyers' Singleton)
 *
 * WHAT: A pattern that ensures a class has only ONE instance globally.
 *
 * HOW:
 *   1. Make the constructor `private`.
 *   2. Delete the Copy Constructor and Copy Assignment Operator (prevent
 * cloning).
 *   3. Use a static local variable inside a static `get()` method.
 *      *Note: In C++11 and above, static local variables are guaranteed to be
 * initialized thread-safely!*
 *
 * WHY: Useful for global resources like a Database Connection Pool or Logger.
 *      Using Meyers' Singleton guarantees perfect thread-safety without
 * manually managing Mutex locks.
 */

class Singleton {
private:
  // 1. Private constructor
  Singleton() { std::cout << "Singleton Instance Created!\n"; }

public:
  // 2. Delete copy constructor and assignment operator to strictly enforce one
  // instance
  Singleton(const Singleton &) = delete;
  Singleton &operator=(const Singleton &) = delete;

  // 3. Global access point (Thread-Safe)
  static Singleton &get() {
    // This static variable is created exactly once.
    // C++11 guarantees this initialization is completely thread-safe.
    static Singleton instance;
    return instance;
  }

  void doWork() { std::cout << "Singleton is working safely\n"; }
};

int main() {
  // We access the singleton via reference
  Singleton::get().doWork();

  // Notice the constructor is NOT called a second time here
  Singleton::get().doWork();

  return 0;
}
