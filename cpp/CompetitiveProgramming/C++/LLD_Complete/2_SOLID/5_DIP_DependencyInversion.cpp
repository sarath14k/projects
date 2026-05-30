// To compile and run: cd
// /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/2_SOLID &&
// g++ -std=c++17 5_DIP_DependencyInversion.cpp -o 5_DIP_DependencyInversion &&
// ./5_DIP_DependencyInversion
#include <iostream>

/*
 * CONCEPT: Dependency Inversion Principle (DIP) - The 'D' in SOLID
 *
 * WHAT: High-level modules should not depend on low-level modules. Both should
 * depend on abstractions. Abstractions should not depend on details. Details
 * should depend on abstractions.
 *
 * HOW: Instead of passing a concrete class (like `ConsoleLogger`) into your
 * App, pass an interface
 *      (`ILogger`). The App relies on the interface, not the exact
 * implementation.
 *
 * WHY: Decouples components. You can easily swap out `ConsoleLog` for `FileLog`
 * or `DatabaseLog` without ever changing the `App` class code.
 */

// Abstraction
class ILogger {
public:
  virtual void log() = 0;
  virtual ~ILogger() {}
};

// Low-level detail depending on abstraction
class ConsoleLog : public ILogger {
public:
  void log() override { std::cout << "Console Logging\n"; }
};

// High-level module depending on abstraction, NOT on ConsoleLog directly
class App {
  ILogger &logger;

public:
  App(ILogger &l) : logger(l) {}
  void run() { logger.log(); }
};

int main() {
  ConsoleLog c;
  App app(c);
  app.run();
  return 0;
}
