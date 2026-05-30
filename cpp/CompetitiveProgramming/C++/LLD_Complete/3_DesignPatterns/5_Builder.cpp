// To compile and run: cd
// /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/3_DesignPatterns
// && g++ -std=c++17 5_Builder.cpp -o 5_Builder && ./5_Builder
#include <iostream>
#include <string>

/*
 * CONCEPT: Builder Design Pattern
 *
 * WHAT: A creational pattern used to construct a complex object step by step.
 *
 * HOW: Separate the construction of a complex object from its representation.
 * You chain methods returning `*this` (or reference) to slowly build the object
 * before finally returning it.
 *
 * WHY: Solves the "Telescoping Constructor" anti-pattern (a constructor with
 * 10+ confusing parameters). It makes object instantiation highly readable and
 * allows for optional parameters easily.
 */

class Computer {
public:
  std::string cpu, ram, storage;
  void show() {
    std::cout << "PC: " << cpu << ", " << ram << ", " << storage << "\n";
  }
};

class ComputerBuilder {
  Computer pc;

public:
  ComputerBuilder &setCPU(std::string cpu) {
    pc.cpu = cpu;
    return *this;
  }
  ComputerBuilder &setRAM(std::string ram) {
    pc.ram = ram;
    return *this;
  }
  ComputerBuilder &setStorage(std::string storage) {
    pc.storage = storage;
    return *this;
  }

  Computer build() { return pc; }
};

int main() {
  // Highly readable chaining to build a complex object
  Computer gamingRig = ComputerBuilder()
                           .setCPU("Intel i9")
                           .setRAM("32GB")
                           .setStorage("2TB NVMe")
                           .build();

  gamingRig.show();
  return 0;
}
