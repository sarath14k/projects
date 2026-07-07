#include <iostream>
#include <string>
using namespace std;

/*
 * ============================================================================
 * DESIGN PATTERN: COFFEE MACHINE SINGLETON (THREAD-SAFE)
 * ============================================================================
 * ANALOGY: Multiple employees (Threads) share exactly ONE breakroom coffee 
 * machine (Instance) instead of building individual ones.
 * ============================================================================
 */

class CoffeeMachine {
private:
    // Lock warehouse: Prevents creating machines outside via 'new'
    CoffeeMachine() { 
        cout << ">> Machine installed in breakroom! <<\n"; 
    }

public:
    // No cloning: Blocks duplicate creations
    CoffeeMachine(const CoffeeMachine&) = delete;
    CoffeeMachine& operator=(const CoffeeMachine&) = delete;

    // Breakroom Door: The single point of access
    static CoffeeMachine& get() {
        // First thread initializes it safely. Subsequent threads wait if needed,
        // then cleanly share this exact same block of memory.
        static CoffeeMachine machine; 
        return machine;
    }

    // Action method
    void brew(const string& user) {
        cout << "[Machine]: Brewed coffee for " << user << "\n";
    }
};

int main() {
    // All calls access the exact same static instance through the short get() method
    CoffeeMachine::get().brew("Alice");
    CoffeeMachine::get().brew("Bob");
    CoffeeMachine::get().brew("Charlie");
    
    return 0;
}
