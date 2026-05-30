// To compile and run: cd /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/5_Modern_CPP && g++ -std=c++17 3_MoveSemantics.cpp -o 3_MoveSemantics && ./3_MoveSemantics
#include <iostream>
#include <vector>
#include <string>

/*
 * CONCEPT: Move Semantics & std::move
 * 
 * --- LVALUE vs RVALUE ---
 * Lvalue (Locator Value): An object with a specific, persistent memory address. 
 *                         It lives beyond a single expression. (e.g., a variable `int x`).
 * Rvalue (Read Value): A temporary object with no persistent memory address. 
 *                      It dies at the end of the expression. (e.g., the number `5`, or `x + y`).
 * ------------------------
 * 
 * WHAT: An optimization technique introduced in C++11 that allows resources to be "moved" 
 *       from a temporary object (rvalue) to another, rather than copying them.
 * 
 * HOW: Implemented using Rvalue references (`&&`) and the move constructor/assignment operator. 
 *      `std::move()` safely casts an lvalue to an rvalue, allowing its resources to be stolen.
 * 
 * WHY: Prevents expensive, unnecessary deep copies when an object is about to be destroyed anyway 
 *      (like returning a large vector from a function). It vastly improves performance.
 */

class LargeData {
public:
    std::string data;

    // Standard Copy Constructor
    LargeData(const std::string& str) : data(str) {
        std::cout << "Data Copied: " << data << "\n";
    }

    // Move Constructor (Takes Rvalue reference &&)
    LargeData(std::string&& str) noexcept : data(std::move(str)) {
        std::cout << "Data MOVED (Stealing resources)\n";
    }
};

int main() {
    std::string tempStr = "Heavy Payload";
    
    // Calls Copy Constructor (tempStr is an lvalue)
    LargeData obj1(tempStr); 
    
    // Calls Move Constructor (std::move casts tempStr to an rvalue)
    LargeData obj2(std::move(tempStr)); 
    
    // tempStr is now empty because its memory was stolen by obj2!
    std::cout << "After move, tempStr length: " << tempStr.length() << "\n";
    
    return 0;
}
