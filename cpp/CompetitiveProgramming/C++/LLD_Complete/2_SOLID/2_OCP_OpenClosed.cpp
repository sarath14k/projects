// To compile and run: cd
// /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/2_SOLID &&
// g++ -std=c++17 2_OCP_OpenClosed.cpp -o 2_OCP_OpenClosed && ./2_OCP_OpenClosed
#include <iostream>

/*
 * CONCEPT: Open/Closed Principle (OCP) - The 'O' in SOLID
 *
 * WHAT: Software entities (classes, modules) should be OPEN for extension but
 * CLOSED for modification.
 *
 * HOW: Use interfaces/abstract classes. When you need new behavior, you create
 * a new class that inherits from the interface, rather than modifying existing,
 * tested code.
 *
 * WHY: Modifying existing code risks breaking current functionality. By
 * extending instead, you safely add new features (like adding a new Shape)
 * without touching existing Shapes.
 */

class Shape {
public:
  virtual double area() const = 0;
  virtual ~Shape() {}
};

class Circle : public Shape {
public:
  double area() const override { return 3.14; }
};

// Adding a new shape doesn't require modifying Shape or Circle classes!
class Rect : public Shape {
public:
  double area() const override { return 4.0; }
};

int main() {
  Circle c;
  Rect r;
  std::cout << "Circle Area: " << c.area() << ", Rect Area: " << r.area()
            << "\n";
  return 0;
}
