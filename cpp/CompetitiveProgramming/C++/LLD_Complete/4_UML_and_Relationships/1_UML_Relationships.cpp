// To compile and run: cd /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/4_UML_and_Relationships && g++ -std=c++17 1_UML_Relationships.cpp -o 1_UML_Relationships && ./1_UML_Relationships
#include <iostream>

/*
 * CONCEPT: UML Relationships (Aggregation vs Composition)
 * 
 * WHAT & HOW:
 *   1. Aggregation ("Has-A", Weak Relationship):
 *      - A class contains a POINTER or REFERENCE to another class.
 *      - If the parent dies, the child CAN STILL EXIST independently.
 *      - Example: Department has Teachers. If the Department closes, Teachers still exist.
 * 
 *   2. Composition ("Part-Of", Strong Relationship):
 *      - A class contains an INSTANCE of another class directly.
 *      - If the parent dies, the child DIES WITH IT.
 *      - Example: House has Rooms. If you destroy the House, the Rooms are destroyed too.
 * 
 * WHY: Crucial for managing memory and understanding the true lifecycle of objects in your system.
 */

class Teacher {};

// AGGREGATION: Department holds pointers to Teachers
class Department { 
    Teacher* t; 
}; 

class Room {};

// COMPOSITION: House physically contains the Room instance
class House { 
    Room r; 
}; 

int main() { 
    std::cout << "UML Relationships: Aggregation vs Composition\n"; 
    return 0; 
}
