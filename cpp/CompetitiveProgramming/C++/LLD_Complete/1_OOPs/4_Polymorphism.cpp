// To compile and run: cd
// /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/1_OOPs &&
// g++ -std=c++17 4_Polymorphism.cpp -o 4_Polymorphism && ./4_Polymorphism
#include <iostream>

/*
 * CONCEPT: Polymorphism (Compile-Time vs Runtime)
 *
 * WHAT: The ability of different objects or functions to behave differently 
 * based on the context. "One interface, multiple implementations."
 *
 * TYPES:
 * 1. Compile-Time (Static) Polymorphism: 
 *    - Resolved by the compiler before the program runs.
 *    - Achieved via Function Overloading (same function name, different parameters) 
 *      or Operator Overloading.
 *    - Fast, but less flexible.
 *
 * 2. Runtime (Dynamic) Polymorphism:
 *    - Resolved by the CPU while the program is actually executing.
 *    - Achieved via `virtual` functions and inheritance. The compiler uses a VTable 
 *      to figure out which exact function to call.
 *    - Slightly slower (due to VTable lookup pointer), but highly flexible.
 */

class Animal {
public:
  // --- COMPILE-TIME POLYMORPHISM (Function Overloading) ---
  // The compiler knows exactly which 'eat' to call based on the arguments passed.
  void eat() { std::cout << "Eating generic food\n"; }
  void eat(std::string foodType) { std::cout << "Eating " << foodType << "\n"; }

  // --- RUNTIME POLYMORPHISM (Virtual Functions) ---
  virtual void sound() { std::cout << "Generic animal sound\n"; }
  virtual ~Animal() {}
};

class Dog : public Animal {
public:
  void sound() override { std::cout << "Bark\n"; }
};

int main() {
  // 1. Demonstrating Compile-Time Polymorphism
  std::cout << "--- Compile-Time Polymorphism ---\n";
  Animal genericAnimal;
  genericAnimal.eat();          // Calls the no-argument version
  genericAnimal.eat("a bone");  // Calls the string-argument version

  // 2. Demonstrating Runtime Polymorphism
  std::cout << "\n--- Runtime Polymorphism ---\n";
  // Base pointer, Derived object
  Animal *a = new Dog();

  // Calls Dog's sound() due to dynamic VTable lookup at runtime
  a->sound();

  delete a;
  return 0;
}
