// To compile and run: cd /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/4_UML_and_Relationships && g++ -std=c++17 2_UML_ParkingLot_CRUD.cpp -o 2_UML_ParkingLot_CRUD && ./2_UML_ParkingLot_CRUD
#include <iostream>

/*
 * CONCEPT: Object-Oriented CRUD (Create, Read, Update, Delete) Basics
 * 
 * WHAT: A minimal representation of state management using a real-world entity (Parking Lot).
 * 
 * HOW: Expose simple methods (`park()`, `unpark()`) that internally update the state 
 *      of member objects (the `Spot`'s `isFree` boolean).
 * 
 * WHY: Demonstrates how Low-Level Design bridges real-world actions to internal data mutations 
 *      while hiding the direct data manipulation from the user.
 */

class Spot { 
public: 
    bool isFree = true; 
};

class ParkingLot {
    Spot spot;
public:
    // Update State -> Park
    void park() { 
        spot.isFree = false; 
        std::cout << "Vehicle Parked. Spot occupied.\n"; 
    }
    
    // Update State -> Unpark
    void unpark() { 
        spot.isFree = true; 
        std::cout << "Vehicle Unparked. Spot freed.\n"; 
    }
};

int main() { 
    ParkingLot p; 
    p.park(); 
    p.unpark(); 
    return 0; 
}
