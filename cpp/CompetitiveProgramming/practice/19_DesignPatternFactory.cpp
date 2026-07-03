#include <iostream>
#include <memory>
#include <string>
#include <string_view>

// ==========================================
// 1. Base Product Interface
// ==========================================
class Item {
public:
    virtual void showDetails() const = 0;
    virtual ~Item() = default; // Essential virtual destructor for polymorphic deletion
};

// ==========================================
// 2. Concrete Products (The Inventory)
// ==========================================
class IPhone13 : public Item {
public:
    void showDetails() const override {
        std::cout << "Rendering: Apple iPhone 13 specification page.\n";
    }
};

class Laptop : public Item {
public:
    void showDetails() const override {
        std::cout << "Rendering: Core i7 Laptop specification page.\n";
    }
};

class Bike : public Item { // Easily pluggable new item without changing client code
public:
    void showDetails() const override {
        std::cout << "Rendering: Mountain Sports Bike specification page.\n";
    }
};

// ==========================================
// 3. The Factory (Decoupled Creation Logic)
// ==========================================
class ItemFactory {
public:
    // Returns a unique_ptr to ensure safe, automatic ownership management
    static std::unique_ptr<Item> getItem(std::string_view itemType) {
        if (itemType == "iphone13") {
            return std::make_unique<IPhone13>();
        } else if (itemType == "laptop") {
            return std::make_unique<Laptop>();
        } else if (itemType == "bike") {
            return std::make_unique<Bike>();
        }
        return nullptr; // Returns safely if item doesn't exist
    }
};

// ==========================================
// 4. Client Application (Amazon App)
// ==========================================
class AmazonApp {
public:
    void searchAndViewProduct(const std::string& query) {
        std::cout << "User searched for: " << query << "\n";
        
        // The app interacts ONLY with the Factory and the Base Interface
        std::unique_ptr<Item> product = ItemFactory::getItem(query);
        
        if (product) {
            product->showDetails();
        } else {
            std::cout << "Error: Product variant not found in inventory!\n";
        }
        std::cout << "--------------------------------------\n";
    }
};

// ==========================================
// Execution Execution
// ==========================================
int main() {
    AmazonApp myApp;

    // Simulating dynamic user searches
    myApp.searchAndViewProduct("iphone13");
    myApp.searchAndViewProduct("bike");
    myApp.searchAndViewProduct("laptop");
    myApp.searchAndViewProduct("spaceship"); // Edge-case: Handles invalid items cleanly

    return 0;
}
