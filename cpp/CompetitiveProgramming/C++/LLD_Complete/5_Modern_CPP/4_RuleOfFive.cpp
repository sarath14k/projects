// To compile and run: cd /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/5_Modern_CPP && g++ -std=c++17 4_RuleOfFive.cpp -o 4_RuleOfFive && ./4_RuleOfFive
#include <iostream>
#include <utility>

/*
 * CONCEPT: Rule of Five (C++11)
 * 
 * WHAT: If a class defines one of the following, it should probably define all five:
 *       1. Destructor
 *       2. Copy Constructor
 *       3. Copy Assignment Operator
 *       4. Move Constructor
 *       5. Move Assignment Operator
 * 
 * HOW: Explicitly define them to manage dynamic resources (like raw pointers) safely, 
 *      or use `= default` / `= delete` to enforce semantics.
 * 
 * WHY: Prevents shallow copy bugs, double-free memory corruption, and memory leaks 
 *      when dealing with classes that manually manage resources on the heap.
 */

class Resource {
    int* data;
public:
    // 1. Constructor
    Resource(int val) : data(new int(val)) { std::cout << "Constructor\n"; }
    
    // 2. Destructor
    ~Resource() { delete data; std::cout << "Destructor\n"; }
    
    // 3. Copy Constructor (Deep Copy)
    Resource(const Resource& other) : data(new int(*other.data)) { std::cout << "Copy Constructor\n"; }
    
    // 4. Copy Assignment (Deep Copy)
    Resource& operator=(const Resource& other) {
        if (this != &other) { delete data; data = new int(*other.data); }
        std::cout << "Copy Assignment\n";
        return *this;
    }
    
    // 5. Move Constructor (Steal Resource)
    Resource(Resource&& other) noexcept : data(other.data) {
        other.data = nullptr;
        std::cout << "Move Constructor\n";
    }
    
    // 6. Move Assignment (Steal Resource)
    Resource& operator=(Resource&& other) noexcept {
        if (this != &other) { delete data; data = other.data; other.data = nullptr; }
        std::cout << "Move Assignment\n";
        return *this;
    }
};

int main() {
    std::cout << "--- Creating a ---\n";
    Resource a(10);           
    
    std::cout << "--- Copying a to b ---\n";
    Resource b = a;           
    
    std::cout << "--- Assigning a to c ---\n";
    Resource c(20);           
    c = a;                    
    
    std::cout << "--- Moving a to d ---\n";
    Resource d = std::move(a);
    
    std::cout << "--- Exiting (Destructors) ---\n";
    return 0;
}
