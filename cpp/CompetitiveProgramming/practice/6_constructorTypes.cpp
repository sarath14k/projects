#include <iostream>
using namespace std;

class Number {
public:
    int* ptr;

    // 1. Default Constructor
    Number() {
        ptr = new int(0);
        cout << "1. Default Constructor called (value = 0)\n";
    }

    // 2. Parameterized Constructor
    Number(int val) {
        ptr = new int(val);
        cout << "2. Parameterized Constructor called (value = " << val << ")\n";
    }

    // 3. Copy Constructor (Deep Copy)
    Number(const Number& other) {
        ptr = new int(*other.ptr); // Allocates fresh memory and copies data
        cout << "3. Copy Constructor called (Deep Copy of " << *ptr << ")\n";
    }

    // 4. Move Constructor (Resource Theft)
    Number(Number&& other) noexcept {
        ptr = other.ptr;         // Steal the memory address pointer
        other.ptr = nullptr;     // Safely nullify old object pointer
        cout << "4. Move Constructor called (Resource stolen)\n";
    }

    // Destructor to prevent memory leaks
    ~Number() {
        if (ptr != nullptr) {
            delete ptr;
        }
    }
};

int main() {
    // Triggers Default
    Number n1; 

    // Triggers Parameterized
    Number n2(42); 

    // Triggers Copy (Creates an exact clone in fresh memory)
    Number n3 = n2; 

    // Triggers Move (Transfers data from n3 to n4 instantly without copying)
    Number n4 = move(n3); 

    return 0;
}
