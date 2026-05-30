// To compile and run: cd /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/5_Modern_CPP && g++ -std=c++17 5_Shallow_vs_DeepCopy.cpp -o 5_Shallow_vs_DeepCopy && ./5_Shallow_vs_DeepCopy
#include <iostream>

/*
 * CONCEPT: Shallow Copy vs Deep Copy
 * 
 * WHAT:
 *   - Shallow Copy: Copies the exact values of the member variables as they are. 
 *                   If a variable is a pointer, it copies the *memory address*. 
 *                   Now BOTH objects point to the EXACT SAME memory on the heap.
 * 
 *   - Deep Copy: Copies the *actual values/data* being pointed to. 
 *                It allocates NEW memory on the heap and copies the contents over.
 * 
 * HOW: The compiler auto-generates a Shallow Copy constructor by default. 
 *      To do a Deep Copy, you MUST write a custom Copy Constructor and allocate `new` memory.
 * 
 * WHY: Shallow copies cause "Double-Free Corruption". When the first object is destroyed, 
 *      it deletes the memory. When the second object is destroyed, it tries to delete 
 *      that same memory AGAIN, crashing the program!
 */

class Shallow {
public:
    int* data;
    Shallow(int v) { data = new int(v); }
    
    // Default compiler-generated copy constructor does exactly this:
    // Shallow(const Shallow& other) { data = other.data; }
    
    ~Shallow() { 
        // WARNING: If copied shallowly, both objects will try to delete the same memory!
        // delete data; // I've commented this out to prevent the actual crash in this demo!
    }
};

class Deep {
public:
    int* data;
    Deep(int v) { data = new int(v); }
    
    // CUSTOM Deep Copy Constructor
    Deep(const Deep& other) { 
        data = new int(*other.data); // Allocate NEW memory, copy the VALUE
    }
    
    ~Deep() { 
        delete data; // Perfectly safe! Each object has its own separate memory.
    }
};

int main() {
    std::cout << "--- Shallow Copy ---\n";
    Shallow s1(10);
    Shallow s2 = s1; // Both s1.data and s2.data point to the SAME address!
    std::cout << "s1 address: " << s1.data << "\n";
    std::cout << "s2 address: " << s2.data << " (Uh oh, they are identical!)\n";
    
    std::cout << "\n--- Deep Copy ---\n";
    Deep d1(20);
    Deep d2 = d1; // d2.data points to a NEW address with the same value!
    std::cout << "d1 address: " << d1.data << " (Value: " << *d1.data << ")\n";
    std::cout << "d2 address: " << d2.data << " (Value: " << *d2.data << ")\n";
    std::cout << "(Safe! They are completely independent.)\n";

    return 0;
}
