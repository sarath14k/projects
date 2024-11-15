#include <iostream>

class Car {
private:
    double mileage;

public:
    Car(double m) : mileage(m) {}
    friend class Mechanic;
    friend double calculateFuelEfficiency(const Car& car);
};

class Mechanic {
public:
    void inspectMileage(const Car& car) {
        std::cout << "Mechanic inspecting mileage: " << car.mileage << " KMs\n";
    }
};

double calculateFuelEfficiency(const Car& car) {
    return car.mileage / 10.0; // Simple efficiency formula for demonstration
}

int main() {
    Car myCar(500); // Car with 500 miles of mileage
    Mechanic mechanic;
    mechanic.inspectMileage(myCar);
    double efficiency = calculateFuelEfficiency(myCar);
    std::cout << "Fuel Efficiency: " << efficiency << " km per litre\n";

    return 0;
}
