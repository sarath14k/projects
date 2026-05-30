// To compile and run: cd /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/7_Templates && g++ -std=c++17 1_Templates.cpp -o 1_Templates && ./1_Templates
#include <iostream>
#include <string>

/*
 * CONCEPT: Templates (Generic Programming)
 * 
 * WHAT: A feature that allows you to write functions or classes that work with any data type.
 * 
 * HOW: Use the `template <typename T>` declaration. The compiler will generate the specific 
 *      version of the function/class at compile-time when you call it with a specific type.
 * 
 * WHY: Prevents code duplication. Instead of writing `int add(int, int)` and `double add(double, double)`, 
 *      you write one generic template that can handle `int`, `double`, `float`, or custom objects.
 */

// Generic Function Template
template <typename T>
T add(T a, T b) {
    return a + b;
}

// Generic Class Template
template <typename T>
class Box {
    T value;
public:
    Box(T v) : value(v) {}
    T getValue() { return value; }
};

int main() {
    // Compiler generates int version
    std::cout << "Int Add: " << add(5, 10) << "\n";
    
    // Compiler generates double version
    std::cout << "Double Add: " << add(5.5, 2.2) << "\n";
    
    Box<std::string> stringBox("Templates are powerful!");
    std::cout << "Box holds: " << stringBox.getValue() << "\n";
    
    return 0;
}
