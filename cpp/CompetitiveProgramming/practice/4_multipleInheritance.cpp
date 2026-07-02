#include <iostream>
using namespace std;

class Car {
public:
    void drive() { cout << "Driving car!\n"; }
};

class Airplane {
public:
    void fly() { cout << "Flying Airplane!\n"; }
};

// Inherits from BOTH classes at the same time
class FlyingCar : public Car, public Airplane {};

int main() {
    FlyingCar obj;
    
    // Calls inherited methods directly
    obj.drive(); // Outputs: Driving car!
    obj.fly();   // Outputs: Flying Airplane!
}
