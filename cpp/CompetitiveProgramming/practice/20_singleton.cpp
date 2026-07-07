#include <iostream>
#include <string>
using namespace std;

/*
 * ============================================================================
 * DESIGN PATTERN: THE OFFICE COFFEE MACHINE (THREAD-SAFE SINGLETON)
 * ============================================================================
 * REAL-WORLD ANALOGY:
 * An office has many employees (Threads). Instead of wasting money buying every 
 * employee an individual desk coffee maker, the office sets up exactly ONE 
 * master coffee machine in the breakroom for everyone to share safely.
 * ============================================================================
 */

class OfficeCoffeeMachine {
private:
    // LIFE EXAMPLE: The warehouse is locked! 
    // Making this constructor 'private' means employees are physically forbidden 
    // from typing 'new OfficeCoffeeMachine()' to build their own private machines.
    OfficeCoffeeMachine() { 
        cout << ">> Breakroom Notice: The official single office coffee machine has been installed! <<\n"; 
    }

public:
    // LIFE EXAMPLE: No cloning or 3D scanning allowed.
    // Deleting these functions ensures nobody can accidentally duplicate or copy 
    // the single breakroom machine.
    OfficeCoffeeMachine(const OfficeCoffeeMachine&) = delete;
    OfficeCoffeeMachine& operator=(const OfficeCoffeeMachine&) = delete;

    // LIFE EXAMPLE: The Breakroom Door.
    // This is the ONLY way for employees to access a coffee machine. 
    static OfficeCoffeeMachine& getBreakroomDoor() {
        // LIFE EXAMPLE: The very first employee to walk through the door in the 
        // morning physically unboxes and boots up this 'static' machine. 
        //
        // THREAD SAFETY: If Employee B walks into the breakroom while Employee A 
        // is still unboxing it, C++11 forces Employee B to pause and wait in line 
        // until the machine is fully ready. After that, everyone uses the exact same one.
        static OfficeCoffeeMachine singleBreakroomMachine; 
        return singleBreakroomMachine;
    }

    // LIFE EXAMPLE: Pressing the brew button.
    // A shared action that any employee can perform once they are inside the breakroom.
    void brewCup(const string& employeeName) {
        cout << "[Machine]: Brewing a fresh cup of coffee for " << employeeName << "\n";
    }
};

int main() {
    // Employee Alice walks to the breakroom door, boots the machine (since she's first), and gets coffee.
    OfficeCoffeeMachine::getBreakroomDoor().brewCup("Alice");
    
    // Employee Bob walks to the breakroom door. He doesn't create a new machine; 
    // he safely uses the exact same machine Alice just set up.
    OfficeCoffeeMachine::getBreakroomDoor().brewCup("Bob");
    
    // Employee Charlie uses the same machine.
    OfficeCoffeeMachine::getBreakroomDoor().brewCup("Charlie");
    
    return 0;
}
