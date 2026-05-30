#include <iostream>
#include <memory> // Required for smart pointers

/*
SMART POINTERS IN C++
1. unique_ptr: Exclusive ownership. No copying, only moving.
2. shared_ptr: Shared ownership. Reference counting tracks users.
3. weak_ptr:   Observer. Doesn't own memory, prevents circular references.
*/

class Entity {
public:
    Entity() { std::cout << "  [Constructor] Entity Created\n"; }
    ~Entity() { std::cout << "  [Destructor] Entity Destroyed\n"; }
    void doSomething() { std::cout << "  Entity is doing something...\n"; }
};

int main() {
    std::cout << "--- 1. std::unique_ptr ---\n";
    {
        // Created using make_unique (preferred for safety and speed)
        std::unique_ptr<Entity> uPtr1 = std::make_unique<Entity>();
        uPtr1->doSomething();

        // std::unique_ptr<Entity> uPtr2 = uPtr1; // COMPILER ERROR: Cannot copy unique_ptr
        
        std::cout << "  Moving ownership from uPtr1 to uPtr2...\n";
        std::unique_ptr<Entity> uPtr2 = std::move(uPtr1); 
        
        if (!uPtr1) std::cout << "  uPtr1 is now null.\n";
        if (uPtr2)  std::cout << "  uPtr2 now owns the Entity.\n";

    } // uPtr2 goes out of scope here -> Entity is automatically DESTROYED.

    std::cout << "\n--- 2. std::shared_ptr ---\n";
    {
        std::shared_ptr<Entity> sPtr1 = std::make_shared<Entity>();
        std::cout << "  Current Ref Count: " << sPtr1.use_count() << "\n";

        {
            std::cout << "  Creating sPtr2 (copy of sPtr1)...\n";
            std::shared_ptr<Entity> sPtr2 = sPtr1; // COPY is allowed!
            std::cout << "  Current Ref Count: " << sPtr1.use_count() << "\n";
        } // sPtr2 is destroyed, but Entity stays alive because sPtr1 still exists.
        
        std::cout << "  sPtr2 destroyed. Current Ref Count: " << sPtr1.use_count() << "\n";
    } // sPtr1 destroyed -> Ref count hits 0 -> Entity is DESTROYED.

    std::cout << "\n--- 3. std::weak_ptr ---\n";
    {
        // Observations without ownership. Used to break circular dependencies.
        std::shared_ptr<Entity> sPtr = std::make_shared<Entity>();
        std::weak_ptr<Entity> wPtr = sPtr; 

        std::cout << "  Ref Count: " << sPtr.use_count() << " (weak_ptr doesn't increase it)\n";

        // To use a weak_ptr, you must convert it back to a shared_ptr using .lock()
        if (auto tempShared = wPtr.lock()) {
            std::cout << "  Accessing Entity via weak_ptr.lock()...\n";
            tempShared->doSomething();
        }

        std::cout << "  Resetting sPtr...\n";
        sPtr.reset(); // Destroy the object

        if (wPtr.expired()) {
            std::cout << "  wPtr.expired() is true. The Entity is gone.\n";
        }
    }

    return 0;
}
