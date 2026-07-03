#include <iostream>
#include <memory>
#include <string>

// Interface
struct Item {
    virtual void show() = 0;
    virtual ~Item() = default;
};

// Concrete Products
struct IPhone : Item { void show() override { std::cout << "iPhone\n"; } };
struct Laptop : Item { void show() override { std::cout << "Laptop\n"; } };

// Factory
struct ItemFactory {
    static std::unique_ptr<Item> getItem(const std::string& type) {
        if (type == "iphone") return std::make_unique<IPhone>();
        if (type == "laptop") return std::make_unique<Laptop>();
        return nullptr;
    }
};

int main() {
    // Client usage decoupled from concrete implementation
    if (auto item = ItemFactory::getItem("iphone")) item->show();
    if (auto item = ItemFactory::getItem("laptop")) item->show();
}
