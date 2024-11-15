#include <iostream>

void printValue(void* ptr, char type) {
    // Function to print the value based on type
    switch (type) {
        case 'i': // Integer
            std::cout << "Integer: " << *(static_cast<int*>(ptr)) << std::endl;
            break;
        case 'f': // Float
            std::cout << "Float: " << *(static_cast<float*>(ptr)) << std::endl;
            break;
        case 'c': // Char
            std::cout << "Char: " << *(static_cast<char*>(ptr)) << std::endl;
            break;
        default:
            std::cout << "Unknown type!" << std::endl;
    }
}

int main() {
    int intValue = 42;
    float floatValue = 3.14f;
    char charValue = 'A';

    void* ptr; // Declare a void pointer

    // Point to an integer
    ptr = &intValue;
    printValue(ptr, 'i');

    // Point to a float
    ptr = &floatValue;
    printValue(ptr, 'f');

    // Point to a char
    ptr = &charValue;
    printValue(ptr, 'c');

    return 0;
}

