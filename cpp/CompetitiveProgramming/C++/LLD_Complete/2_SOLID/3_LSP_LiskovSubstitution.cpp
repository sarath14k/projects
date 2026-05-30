// To compile and run: cd
// /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/2_SOLID &&
// g++ -std=c++17 3_LSP_LiskovSubstitution.cpp -o 3_LSP_LiskovSubstitution &&
// ./3_LSP_LiskovSubstitution
#include <iostream>

/*
 * CONCEPT: Liskov Substitution Principle (LSP) - The 'L' in SOLID
 *
 * WHAT: Objects of a superclass should be replaceable with objects of its
 * subclasses without breaking the application.
 *
 * HOW: Subclasses must strictly honor the contract established by the base
 * class. If a Base class guarantees a behavior (like `fly()`), a subclass
 * cannot throw an exception or fail to perform that behavior (like an Ostrich
 * subclass).
 *
 * WHY: Ensures predictability. Code that uses the Base class pointer shouldn't
 * have to guess if the specific subclass will crash or behave entirely
 * differently.
 */

class Bird {
public:
  virtual void fly() = 0;
  virtual ~Bird() {}
};

class Sparrow : public Bird {
public:
  void fly() override { std::cout << "Sparrow flies normally\n"; }
};

// Notice we do NOT have an Ostrich class inheriting Bird,
// because Ostrich cannot fly, which would violate LSP!

int main() {
  Bird *b = new Sparrow();

  // We can confidently call fly() without worrying about which bird it is
  b->fly();

  delete b;
  return 0;
}
