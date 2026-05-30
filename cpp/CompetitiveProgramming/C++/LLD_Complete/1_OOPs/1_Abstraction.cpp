// To compile and run: cd
// /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/1_OOPs &&
// g++ -std=c++17 1_Abstraction.cpp -o 1_Abstraction && ./1_Abstraction
#include <iostream>

/*
 * CONCEPT: Abstraction
 *
 * WHAT: Hiding the complex internal implementation details and exposing only
 * the essential features to the user.
 *
 * HOW: Achieved using access modifiers (private/protected). The internal
 * workings are kept `private`, while the interface the user interacts with is
 * made `public`.
 *
 * WHY: Reduces complexity for the user. The user doesn't need to know *how* the
 * engine starts, only that they can call `start()`. It also protects internal
 * state from unintended interference.
 */

class Car {
private:
  // Internal detail hidden from the user
  void igniteEngine() { std::cout << "Spark plugs fired, fuel injected...\n"; }

public:
  // Exposed functionality
  void start() {
    igniteEngine();
    std::cout << "Car started\n";
  }
};

int main() {
  Car c;
  c.start(); // User only knows about start()
  return 0;
}
