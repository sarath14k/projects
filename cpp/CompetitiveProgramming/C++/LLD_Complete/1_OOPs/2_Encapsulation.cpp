// To compile and run: cd
// /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/1_OOPs &&
// g++ -std=c++17 2_Encapsulation.cpp -o 2_Encapsulation && ./2_Encapsulation
#include <iostream>

/*
 * CONCEPT: Encapsulation
 *
 * WHAT: Bundling data (variables) and methods (functions) that operate on the
 * data into a single unit (class), and restricting direct access to some of the
 * object's components.
 *
 * HOW: Achieved by making class attributes `private` and providing `public`
 * getter and setter methods to read or modify those attributes safely.
 *
 * WHY: Protects an object's internal state from invalid changes. For example,
 * preventing a negative balance from being set directly.
 */

class BankAccount {
private:
  int balance = 0; // Data is hidden

public:
  // Controlled access to modify data
  void deposit(int amt) {
    if (amt > 0) {
      balance += amt;
    }
  }

  // Controlled access to read data
  int getBalance() const { return balance; }
};

int main() {
  BankAccount b;
  b.deposit(100);
  std::cout << "Balance: " << b.getBalance() << "\n";
  return 0;
}
