// To compile and run: cd
// /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/1_OOPs &&
// g++ -std=c++17 6_Virtual_vs_PureVirtual.cpp -o 6_Virtual_vs_PureVirtual &&
// ./6_Virtual_vs_PureVirtual
#include <iostream>

/*
 * CONCEPT: Virtual vs Pure Virtual Functions
 *
 * WHAT & HOW:
 *   - Virtual Function: `virtual void func() {}` -> Has a default
 * implementation. Derived classes CAN override it, but don't have to.
 *   - Pure Virtual Function: `virtual void func() = 0;` -> Has NO
 * implementation. Derived classes MUST override it.
 *
 * WHY:
 *   - Use a standard virtual function when most children share the same
 * behavior, but some might differ.
 *   - Use a pure virtual function to enforce a strict contract (Interface),
 * ensuring all children define that specific behavior themselves. A class with
 * a pure virtual function becomes Abstract.
 */

class Base {
public:
  // Standard virtual: Default behavior provided
  virtual void standard() { std::cout << "Standard Virtual\n"; }

  // Pure virtual: Forces derived classes to implement this
  virtual void pure() = 0;

  virtual ~Base() {}
};

class Derived : public Base {
public:
  // Mandatory override
  void pure() override { std::cout << "Pure Implemented\n"; }
};

int main() {
  Base *b = new Derived();
  b->standard(); // Uses base implementation
  b->pure();     // Uses derived implementation
  delete b;
  return 0;
}
