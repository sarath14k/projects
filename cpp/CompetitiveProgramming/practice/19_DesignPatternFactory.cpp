#include <iostream>
#include <memory> // Required for std::unique_ptr and std::make_unique
#include <string>
using namespace std;

/* 
 * ============================================================================
 * DESIGN PATTERN NOTES: THE FACTORY METHOD (CREATIONAL)
 * ============================================================================
 * PURPOSE:
 * Provides an interface for creating objects, but lets the factory decide 
 * which concrete class to instantiate. It decouples the client code (main) 
 * from the actual object creation logic.
 * 
 * BENEFITS SHOWN HERE:
 * 1. Loose Coupling: main() only interacts with 'Item', not 'IPhone' or 'Laptop'.
 * 2. Single Responsibility: Object creation logic lives strictly inside 'ItemFactory'.
 * 3. Open/Closed Principle: To add a new product (e.g., Tablet), you just create 
 *    the struct and add an 'if' in the factory. main() remains untouched.
 * ============================================================================
 */

// --- Component 1: The Abstract Product (Interface) ---
// Defines the common behavior for all objects the factory can build.
struct Item {
	// Pure virtual function forces derived classes to implement their own version.
	virtual void show() = 0;
	
	// DESIGN NOTE: The Virtual Destructor is CRITICAL here. 
	// Because we use polymorphism (managing derived objects via a base pointer), 
	// a virtual destructor ensures that when unique_ptr deletes the 'Item', 
	// the proper derived destructor (IPhone or Laptop) is called, preventing leaks.
	virtual ~Item() = default;
};

// --- Component 2: Concrete Products ---
// The actual specific objects created by the factory that implement the interface.
struct IPhone : Item {
	void show() override { cout << "IPhone\n"; }
};

struct Laptop : Item {
	void show() override { cout << "Laptop\n"; }
};

// --- Component 3: The Creator / Factory ---
// Encapsulates the conditional creation logic.
struct ItemFactory {
	// MODERN C++ NOTE: Returns a std::unique_ptr instead of a raw pointer (Item*).
	// This explicitly transfers single ownership to the caller. The client code 
	// doesn't have to remember to manually call 'delete', preventing memory leaks.
	static unique_ptr<Item> getItem(const string& type) {
		if (type == "iphone") return make_unique<IPhone>();
		if (type == "laptop") return make_unique<Laptop>();
		return nullptr; // Safe fallback if an invalid type string is requested.
	}
};

// --- Component 4: The Client ---
int main()
{
	// C++17 NOTE: Selection statement with initializer.
	// We initialize 'item' and check if it's not null inside the 'if' condition.
	// This limits the scope of 'item' strictly to this block, which is excellent 
	// practice for keeping variable lifetimes short and predictable.
	if (auto item = ItemFactory::getItem("iphone"))
		item->show(); // Polymorphism: Resolves to IPhone::show() at runtime.
		
	if (auto item = ItemFactory::getItem("laptop"))
		item->show(); // Polymorphism: Resolves to Laptop::show() at runtime.
		
	return 0;
	// AUTOMATIC CLEANUP: As 'main' ends, the unique_ptrs leave their scope. 
	// They automatically trigger the virtual destructors, cleanly destroying the 
	// allocated IPhone and Laptop objects with zero manual effort.
}
