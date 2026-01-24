#include <iostream>
#include <cstring>

class String {
private:
    char* data; // Pointer to dynamically allocated memory

public:
    // Default constructor
    String() : data(nullptr) {}

    // Parameterized constructor
    String(const char* str) {
        if (str) {
            data = new char[strlen(str) + 1]; // Allocate memory
            strcpy(data, str); // Copy the string
        } else {
            data = nullptr;
        }
    }

    // Copy constructor
    String(const String& other) {
        if (other.data) {
            data = new char[strlen(other.data) + 1]; // Allocate memory
            strcpy(data, other.data); // Copy the string
        } else {
            data = nullptr;
        }
    }

    // Move constructor
    String(String&& other) noexcept : data(other.data) {
        other.data = nullptr; // Leave other in a valid state
    }

    // Assignment operator
    String& operator=(const String& other) {
        if (this != &other) { // Self-assignment check
            delete[] data; // Free existing memory
            if (other.data) {
                data = new char[strlen(other.data) + 1]; // Allocate memory
                strcpy(data, other.data); // Copy the string
            } else {
                data = nullptr;
            }
        }
        return *this; // Return *this to allow chained assignments
    }

    // Move assignment operator
    String& operator=(String&& other) noexcept {
        if (this != &other) { // Self-assignment check
            delete[] data; // Free existing memory
            data = other.data; // Steal the data
            other.data = nullptr; // Leave other in a valid state
        }
        return *this; // Return *this to allow chained assignments
    }

    // Destructor
    ~String() {
        delete[] data; // Free allocated memory
    }

    // Function to display the string
    void display() const {
        if (data) {
            std::cout << "String: " << data << std::endl;
        } else {
            std::cout << "String is empty." << std::endl;
        }
    }
};

int main() {
    // Default constructor
    String defaultStr;
    std::cout << "Created defaultStr using Default Constructor." << std::endl;
    defaultStr.display();

    // Parameterized constructor
    String paramStr("Hello, World!");
    std::cout << "Created paramStr using Parameterized Constructor." << std::endl;
    paramStr.display();

    // Copy constructor
    String copyStr(paramStr);
    std::cout << "Created copyStr using Copy Constructor." << std::endl;
    copyStr.display();

    // Move constructor
    String movedStr(std::move(paramStr));
    std::cout << "Created movedStr using Move Constructor." << std::endl;
    movedStr.display();
    std::cout << "paramStr after move (should be empty):" << std::endl;
    paramStr.display(); // Should be empty now

    // Assignment operator
    String assignedStr;
    assignedStr = copyStr;  // Assigning using assignment operator
    std::cout << "Assigned copyStr to assignedStr using Copy Assignment Operator." << std::endl;
    assignedStr.display();

    // Move assignment operator
    String anotherStr;
    anotherStr = std::move(assignedStr); // Move assignment
    std::cout << "Moved assignedStr to anotherStr using Move Assignment Operator." << std::endl;
    anotherStr.display();
    std::cout << "assignedStr after move (should be empty):" << std::endl;
    assignedStr.display(); // Should be empty now

    return 0;
}

