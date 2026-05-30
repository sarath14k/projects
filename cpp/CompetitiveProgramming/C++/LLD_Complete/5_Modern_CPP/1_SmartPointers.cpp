// To compile and run: cd /home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete/5_Modern_CPP && g++ -std=c++17 1_SmartPointers.cpp -o 1_SmartPointers && ./1_SmartPointers
#include <iostream>
#include <memory>

/*
 * CONCEPT: Smart Pointers (Memory Management)
 * 
 * WHAT: Objects that act like pointers but automatically manage the memory they point to, 
 *       ensuring no memory leaks occur.
 * 
 * HOW: 
 *   - std::unique_ptr: Exclusive ownership. Only one unique_ptr can point to the object.
 *   - std::shared_ptr: Shared ownership. Keeps a reference count. Deletes memory when count reaches 0.
 *   - std::weak_ptr: Observes a shared_ptr without increasing the reference count (solves cyclic dependencies).
 * 
 * WHY: Raw pointers (`new` / `delete`) are prone to memory leaks (e.g., forgetting to call `delete`) 
 *      and dangling pointers.
 * 
 * HOW IT AUTOMATES RAII: 
 *   - The smart pointer itself is a stack-allocated object.
 *   - When it is created, it takes ownership of your heap memory (Resource Acquisition).
 *   - Because it lives on the stack, C++ automatically calls its destructor when it goes out of scope.
 *   - Inside its destructor, it automatically calls `delete` on the heap memory it was holding.
 *   - This guarantees the heap memory is freed even if the function crashes or returns early!
 */

class Resource {
public:
    Resource() { std::cout << "Resource Acquired\n"; }
    ~Resource() { std::cout << "Resource Destroyed\n"; }
    void use() { std::cout << "Using Resource\n"; }
};

int main() {
    std::cout << "--- Unique Pointer ---\n";
    {
        std::unique_ptr<Resource> uPtr1 = std::make_unique<Resource>();
        uPtr1->use();
        
        // Ownership MUST be explicitly transferred using std::move
        std::unique_ptr<Resource> uPtr2 = std::move(uPtr1);
        
        if (!uPtr1) std::cout << "uPtr1 is now empty (ownership moved)\n";
        uPtr2->use(); // uPtr2 now owns the memory
    } // Memory automatically freed here by uPtr2

    std::cout << "\n--- Shared Pointer ---\n";
    {
        std::shared_ptr<Resource> sPtr1 = std::make_shared<Resource>();
        {
            std::shared_ptr<Resource> sPtr2 = sPtr1; // Reference count = 2
            std::cout << "Use Count: " << sPtr1.use_count() << "\n";
        } // sPtr2 destroyed, count = 1
        std::cout << "Use Count: " << sPtr1.use_count() << "\n";
    } // sPtr1 destroyed, count = 0, Memory automatically freed here

    std::cout << "\n--- Weak Pointer ---\n";
    {
        std::shared_ptr<Resource> sPtr = std::make_shared<Resource>();
        std::weak_ptr<Resource> wPtr = sPtr; // Does NOT increase reference count!
        
        std::cout << "Use Count after weak_ptr created: " << sPtr.use_count() << "\n";
        
        // Must 'lock()' to convert to shared_ptr before using it safely
        if(std::shared_ptr<Resource> temp = wPtr.lock()) {
            std::cout << "Resource is alive, safely locked!\n";
            temp->use();
        }
    }

    return 0;
}
