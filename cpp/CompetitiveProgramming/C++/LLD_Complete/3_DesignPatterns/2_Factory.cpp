// To compile and run: cd /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/3_DesignPatterns && g++ -std=c++17 2_Factory.cpp -o 2_Factory && ./2_Factory
#include <iostream>

/*
 * CONCEPT: Factory Method Design Pattern
 * 
 * WHAT: A creational pattern that provides an interface for creating objects, but allows 
 *       subclasses or factory classes to alter the type of objects that will be created.
 * 
 * HOW: Instead of calling `new Sedan()` directly in your main code, you call a static 
 *      method `CarFactory::makeCar()`. The factory encapsulates the `new` keyword logic.
 * 
 * WHY: Centralizes object creation. If object creation gets complex, or if you want to 
 *      decide which object to return based on conditions, you do it in ONE place (the Factory).
 */

class Car { 
public: 
    virtual void drive() = 0; 
    virtual ~Car(){} 
};

class Sedan : public Car { 
public: 
    void drive() override { 
        std::cout << "Driving Sedan\n"; 
    } 
};

// Encapsulates object creation
class CarFactory {
public: 
    static Car* makeCar() { 
        return new Sedan(); // Could easily be swapped or contain logic
    }
};

int main() { 
    // Client code doesn't use 'new', it asks the factory
    Car* c = CarFactory::makeCar(); 
    c->drive(); 
    delete c; 
    return 0; 
}
