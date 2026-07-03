#include <iostream> // For std::cout to print text to the console
#include <memory>   // For std::unique_ptr and std::make_unique (smart pointers)
#include <string>   // For std::string to store and compare text strings

// Interface: Defines the common abstract base class for all products
struct Item {
    virtual void show() = 0;        // Pure virtual function making this an interface; must be implemented by child classes
    
    // Virtual destructor ensuring safe cleanup of child objects via base pointers.
    // Without 'virtual', deleting a child object through an Item* pointer would only call ~Item()
    // and completely skip the child class destructor (e.g., ~IPhone()), causing a partial memory leak.
    // '= default' tells the compiler to automatically generate the standard cleanup code for us.
    virtual ~Item() = default;      
};

// Concrete Product 1: Inherits from Item and overrides show() for the iPhone implementation
struct IPhone : Item { 
    void show() override { std::cout << "iPhone\n"; } // Prints "iPhone" when called
};

// Concrete Product 2: Inherits from Item and overrides show() for the Laptop implementation
struct Laptop : Item { 
    void show() override { std::cout << "Laptop\n"; } // Prints "Laptop" when called
};

// Factory: Responsible for abstracting and managing object creation
struct ItemFactory {
    // Static method that takes a string reference and returns a managed smart pointer to an Item
    static std::unique_ptr<Item> getItem(const std::string& type) {
        if (type == "iphone") return std::make_unique<IPhone>(); // If type matches, instantiates and returns an IPhone
        if (type == "laptop") return std::make_unique<Laptop>(); // If type matches, instantiates and returns a Laptop
        return nullptr;                                          // Returns an empty smart pointer if no match is found
    }
};

int main() {
    // Requests an "iphone" from the factory; if it successfully returns a pointer, executes the block
    if (auto item = ItemFactory::getItem("iphone")) 
        item->show(); // Calls the polymorphic show() function of the created iPhone object
        
    // Requests a "laptop" from the factory; if it successfully returns a pointer, executes the block
    if (auto item = ItemFactory::getItem("laptop")) 
        item->show(); // Calls the polymorphic show() function of the created Laptop object
}
