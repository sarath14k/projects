// To compile and run: cd /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/1_OOPs && g++ -std=c++17 5_VTable_VPointer.cpp -o 5_VTable_VPointer && ./5_VTable_VPointer
#include <iostream>

/*
 * CONCEPT: VTable (Virtual Table) & VPointer (Virtual Pointer)
 * 
 * WHAT: The underlying mechanism C++ uses to implement Runtime Polymorphism (Dynamic Binding).
 * 
 * HOW: 
 *   1. VTable: The compiler creates an array of function pointers (VTable) for any class containing virtual functions.
 *   2. VPointer (vptr): The compiler injects a hidden pointer into objects of the class, pointing to the VTable.
 *   When a virtual function is called, C++ follows the vptr to the VTable to find the correct actual function address.
 * 
 * WHY: This is the exact machinery that allows a Base class pointer to correctly execute a Derived class's 
 *      overridden method at runtime.
 */

class Base { 
public: 
    virtual void show() { 
        std::cout << "Base\n"; 
    } 
    virtual ~Base(){} 
};

class Derived : public Base { 
public: 
    void show() override { 
        std::cout << "Derived\n"; 
    } 
};

int main() { 
    Base* b = new Derived(); 
    
    // At runtime, C++ looks at the object's vptr -> VTable -> Derived::show()
    b->show(); 
    
    delete b; 
    return 0; 
}
