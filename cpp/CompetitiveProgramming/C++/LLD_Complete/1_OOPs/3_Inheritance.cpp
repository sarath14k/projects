// To compile and run: cd
// /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/1_OOPs &&
// g++ -std=c++17 3_Inheritance.cpp -o 3_Inheritance && ./3_Inheritance
#include <iostream>

/*
 * CONCEPT: Inheritance
 *
 * WHAT: A mechanism where a new class (Derived/Child) inherits properties and
 * behaviors (methods) from an existing class (Base/Parent).
 *
 * HOW: Using the `:` operator followed by the access specifier and the base
 * class name (e.g., `class Dog : public Animal`).
 *
 * WHY: Promotes code reusability. Common logic can be written once in the Base
 * class and automatically shared with all Derived classes, preventing code
 * duplication.
 */

class Animal {
public:
  void eat() { std::cout << "Eating\n"; }
};

// Dog inherits eat() from Animal
class Dog : public Animal {
public:
  void bark() { std::cout << "Barking\n"; }
};

int main() {
  Dog d;
  d.eat();  // Inherited method
  d.bark(); // Own method
  return 0;
}
