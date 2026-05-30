// To compile and run: cd
// /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/2_SOLID &&
// g++ -std=c++17 4_ISP_InterfaceSegregation.cpp -o 4_ISP_InterfaceSegregation
// && ./4_ISP_InterfaceSegregation
#include <iostream>

/*
 * CONCEPT: Interface Segregation Principle (ISP) - The 'I' in SOLID
 *
 * WHAT: Clients should not be forced to depend on interfaces (methods) they do
 * not use.
 *
 * HOW: Split large, "fat" interfaces into smaller, more specific ones.
 *      Instead of one giant `IMachine` interface with print(), scan(), and
 * fax(), create `IPrinter`, `IScanner`, etc.
 *
 * WHY: If a class only needs to print, it shouldn't be forced to provide empty,
 *      dummy implementations for scan() or fax() just to satisfy the compiler.
 */

// Specific, segregated interfaces
class IPrinter {
public:
  virtual void print() = 0;
  virtual ~IPrinter() {}
};

class IScanner {
public:
  virtual void scan() = 0;
  virtual ~IScanner() {}
};

// Only inherits what it actually uses
class SimplePrinter : public IPrinter {
public:
  void print() override { std::cout << "Printing document\n"; }
};

int main() {
  SimplePrinter p;
  p.print();
  return 0;
}
