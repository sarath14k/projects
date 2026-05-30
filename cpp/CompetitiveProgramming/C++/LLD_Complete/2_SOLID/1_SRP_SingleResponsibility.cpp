// To compile and run: cd
// /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/2_SOLID &&
// g++ -std=c++17 1_SRP_SingleResponsibility.cpp -o 1_SRP_SingleResponsibility
// && ./1_SRP_SingleResponsibility
#include <iostream>

/*
 * CONCEPT: Single Responsibility Principle (SRP) - The 'S' in SOLID
 *
 * WHAT: A class should have one, and only one, reason to change.
 *       It should be responsible for exactly one aspect of the software's
 * functionality.
 *
 * HOW: Instead of putting unrelated behaviors (like data storage, calculations,
 * and printing) into a single massive class, split them into multiple smaller
 * classes.
 *
 * WHY: Makes the system easier to maintain, test, and understand. If tax rules
 * change, you only update TaxCalc, leaving the Order class entirely untouched.
 */

// Responsibility 1: Hold order data
class Order {
public:
  double price = 100.0;
};

// Responsibility 2: Calculate tax
class TaxCalc {
public:
  double getTax(const Order &o) { return o.price * 0.18; }
};

int main() {
  Order o;
  TaxCalc t;
  std::cout << "Tax: " << t.getTax(o) << "\n";
  return 0;
}
