// To compile and run: cd /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/3_DesignPatterns && g++ -std=c++17 4_Strategy.cpp -o 4_Strategy && ./4_Strategy
#include <iostream>

/*
 * CONCEPT: Strategy Design Pattern
 * 
 * WHAT: A behavioral pattern that lets you define a family of algorithms, put each of them 
 *       into a separate class, and make their objects interchangeable at runtime.
 * 
 * HOW: Create a common `Strategy` interface. Create concrete classes implementing that interface. 
 *      A `Context` object holds a pointer to a `Strategy` and uses it to execute the behavior.
 * 
 * WHY: Replaces giant `if-else` or `switch` statements for picking algorithms. You can swap 
 *      behaviors (like Sorting algorithms, or Routing methods) dynamically at runtime.
 */

class Strategy { 
public: 
    virtual void execute() = 0; 
    virtual ~Strategy(){} 
};

// Concrete Strategy A
class FastStrategy : public Strategy { 
public: 
    void execute() override { 
        std::cout << "Executing Fast Strategy Algorithm\n"; 
    } 
};

// The Context runs the assigned strategy
class Context {
    Strategy* s;
public:
    void set(Strategy* strat) { 
        s = strat; 
    }
    void run() { 
        if(s) s->execute(); 
    }
};

int main() { 
    FastStrategy f; 
    Context c; 
    
    c.set(&f); // Swap behavior at runtime
    c.run(); 
    
    return 0; 
}
