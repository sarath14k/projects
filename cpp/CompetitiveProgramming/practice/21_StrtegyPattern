#include <iostream>
#include <memory>

/**
 * WHAT IT IS: 
 * An interface that defines a generic action or behavior.
 * * WHY IT'S USEFUL: 
 * It decouples the context (the runner) from the actual implementation. 
 * Instead of hardcoding behavior, you program to this interface.
 */
struct Strategy { 
    virtual void run() = 0; 
};

/**
 * SPECIALITY: Open/Closed Principle
 * You can add endless new strategies (e.g., StrategyC, StrategyD) 
 * without modifying any existing classes or breaking main code.
 */
struct StrategyA : Strategy { 
    void run() override { std::cout << "Logic A\n"; } 
};

struct StrategyB : Strategy { 
    void run() override { std::cout << "Logic B\n"; } 
};

int main() {
    // SPECIALITY: Runtime Flexibility
    // You can swap the algorithm dynamically at any point during execution.
    
    std::unique_ptr<Strategy> s = std::make_unique<StrategyA>();
    s->run(); // Executes Logic A
    
    // Changing behavior instantly without using an 'if-else' or 'switch'
    s = std::make_unique<StrategyB>(); 
    s->run(); // Executes Logic B
}
