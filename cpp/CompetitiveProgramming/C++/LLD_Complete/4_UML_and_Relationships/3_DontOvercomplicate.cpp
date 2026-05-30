// To compile and run: cd /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/4_UML_and_Relationships && g++ -std=c++17 3_DontOvercomplicate.cpp -o 3_DontOvercomplicate && ./3_DontOvercomplicate
#include <iostream>

/*
 * CONCEPT: KISS Principle (Keep It Simple, Stupid) & YAGNI (You Aren't Gonna Need It)
 * 
 * WHAT: Avoiding over-engineering. Do not build massive abstract hierarchies, complex 
 *       factories, or extensive observer systems if a simple class or function will suffice.
 * 
 * HOW: Write the minimal amount of code to solve the current problem. Refactor to introduce 
 *      design patterns ONLY when the codebase organically demands it due to scaling complexity.
 * 
 * WHY: Over-engineered code is harder to read, harder to debug, and slower to compile. 
 *      Simplicity is the ultimate sophistication.
 */

int main() { 
    std::cout << "KISS: Keep It Simple, Stupid. Only use patterns when necessary.\n"; 
    return 0; 
}
