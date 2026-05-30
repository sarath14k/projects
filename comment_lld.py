import os

base_dir = "/home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete"

files = {
"1_OOPs/1_Abstraction.cpp": """#include <iostream>

/*
 * CONCEPT: Abstraction
 * 
 * WHAT: Hiding the complex internal implementation details and exposing only the essential features to the user.
 * 
 * HOW: Achieved using access modifiers (private/protected). The internal workings are kept `private`, while 
 *      the interface the user interacts with is made `public`.
 * 
 * WHY: Reduces complexity for the user. The user doesn't need to know *how* the engine starts, 
 *      only that they can call `start()`. It also protects internal state from unintended interference.
 */

class Car {
private:
    // Internal detail hidden from the user
    void igniteEngine() { 
        /* complex ignition logic */ 
    }
public:
    // Exposed functionality
    void start() { 
        igniteEngine(); 
        std::cout << "Car started\\n"; 
    }
};

int main() { 
    Car c; 
    c.start(); // User only knows about start()
    return 0; 
}
""",

"1_OOPs/2_Encapsulation.cpp": """#include <iostream>

/*
 * CONCEPT: Encapsulation
 * 
 * WHAT: Bundling data (variables) and methods (functions) that operate on the data into a single unit (class), 
 *       and restricting direct access to some of the object's components.
 * 
 * HOW: Achieved by making class attributes `private` and providing `public` getter and setter methods to 
 *      read or modify those attributes safely.
 * 
 * WHY: Protects an object's internal state from invalid changes. For example, preventing a negative balance 
 *      from being set directly.
 */

class BankAccount {
private:
    int balance = 0; // Data is hidden

public:
    // Controlled access to modify data
    void deposit(int amt) { 
        if(amt > 0) {
            balance += amt; 
        }
    }
    
    // Controlled access to read data
    int getBalance() const { 
        return balance; 
    }
};

int main() { 
    BankAccount b; 
    b.deposit(100); 
    std::cout << "Balance: " << b.getBalance() << "\\n"; 
    return 0; 
}
""",

"1_OOPs/3_Inheritance.cpp": """#include <iostream>

/*
 * CONCEPT: Inheritance
 * 
 * WHAT: A mechanism where a new class (Derived/Child) inherits properties and behaviors (methods) 
 *       from an existing class (Base/Parent).
 * 
 * HOW: Using the `:` operator followed by the access specifier and the base class name (e.g., `class Dog : public Animal`).
 * 
 * WHY: Promotes code reusability. Common logic can be written once in the Base class and automatically 
 *      shared with all Derived classes, preventing code duplication.
 */

class Animal { 
public: 
    void eat() { 
        std::cout << "Eating\\n"; 
    } 
};

// Dog inherits eat() from Animal
class Dog : public Animal { 
public: 
    void bark() { 
        std::cout << "Barking\\n"; 
    } 
};

int main() { 
    Dog d; 
    d.eat();  // Inherited method
    d.bark(); // Own method
    return 0; 
}
""",

"1_OOPs/4_Polymorphism.cpp": """#include <iostream>

/*
 * CONCEPT: Polymorphism
 * 
 * WHAT: The ability of different objects to respond in their own specific way to the same method call.
 *       "One interface, multiple implementations."
 * 
 * HOW: Achieved through `virtual` functions in the Base class and `override` functions in the Derived classes.
 *      A Base class pointer can point to a Derived class object, and the correct overridden method is called at runtime.
 * 
 * WHY: Allows you to write generic code that can work with objects of multiple types without needing to 
 *      know their exact type at compile time.
 */

class Animal { 
public: 
    virtual void sound() { 
        std::cout << "Generic animal sound\\n"; 
    } 
    virtual ~Animal() {} 
};

class Dog : public Animal { 
public: 
    void sound() override { 
        std::cout << "Bark\\n"; 
    } 
};

int main() { 
    // Base pointer, Derived object
    Animal* a = new Dog(); 
    
    // Calls Dog's sound() due to polymorphism
    a->sound(); 
    
    delete a; 
    return 0; 
}
""",

"1_OOPs/5_VTable_VPointer.cpp": """#include <iostream>

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
        std::cout << "Base\\n"; 
    } 
    virtual ~Base(){} 
};

class Derived : public Base { 
public: 
    void show() override { 
        std::cout << "Derived\\n"; 
    } 
};

int main() { 
    Base* b = new Derived(); 
    
    // At runtime, C++ looks at the object's vptr -> VTable -> Derived::show()
    b->show(); 
    
    delete b; 
    return 0; 
}
""",

"1_OOPs/6_Virtual_vs_PureVirtual.cpp": """#include <iostream>

/*
 * CONCEPT: Virtual vs Pure Virtual Functions
 * 
 * WHAT & HOW:
 *   - Virtual Function: `virtual void func() {}` -> Has a default implementation. 
 *                       Derived classes CAN override it, but don't have to.
 *   - Pure Virtual Function: `virtual void func() = 0;` -> Has NO implementation. 
 *                            Derived classes MUST override it.
 * 
 * WHY: 
 *   - Use a standard virtual function when most children share the same behavior, but some might differ.
 *   - Use a pure virtual function to enforce a strict contract (Interface), ensuring all children define 
 *     that specific behavior themselves. A class with a pure virtual function becomes Abstract.
 */

class Base {
public:
    // Standard virtual: Default behavior provided
    virtual void standard() { 
        std::cout << "Standard Virtual\\n"; 
    }
    
    // Pure virtual: Forces derived classes to implement this
    virtual void pure() = 0; 
    
    virtual ~Base(){}
};

class Derived : public Base {
public:
    // Mandatory override
    void pure() override { 
        std::cout << "Pure Implemented\\n"; 
    }
};

int main() { 
    Base* b = new Derived(); 
    b->standard(); // Uses base implementation
    b->pure();     // Uses derived implementation
    delete b; 
    return 0; 
}
""",

"2_SOLID/1_SRP_SingleResponsibility.cpp": """#include <iostream>

/*
 * CONCEPT: Single Responsibility Principle (SRP) - The 'S' in SOLID
 * 
 * WHAT: A class should have one, and only one, reason to change. 
 *       It should be responsible for exactly one aspect of the software's functionality.
 * 
 * HOW: Instead of putting unrelated behaviors (like data storage, calculations, and printing) 
 *      into a single massive class, split them into multiple smaller classes.
 * 
 * WHY: Makes the system easier to maintain, test, and understand. If tax rules change, 
 *      you only update TaxCalc, leaving the Order class entirely untouched.
 */

// Responsibility 1: Hold order data
class Order { 
public: 
    double price = 100.0; 
};

// Responsibility 2: Calculate tax
class TaxCalc { 
public: 
    double getTax(const Order& o) { 
        return o.price * 0.18; 
    } 
};

int main() { 
    Order o; 
    TaxCalc t; 
    std::cout << "Tax: " << t.getTax(o) << "\\n"; 
    return 0; 
}
""",

"2_SOLID/2_OCP_OpenClosed.cpp": """#include <iostream>

/*
 * CONCEPT: Open/Closed Principle (OCP) - The 'O' in SOLID
 * 
 * WHAT: Software entities (classes, modules) should be OPEN for extension but CLOSED for modification.
 * 
 * HOW: Use interfaces/abstract classes. When you need new behavior, you create a new class 
 *      that inherits from the interface, rather than modifying existing, tested code.
 * 
 * WHY: Modifying existing code risks breaking current functionality. By extending instead, 
 *      you safely add new features (like adding a new Shape) without touching existing Shapes.
 */

class Shape { 
public: 
    virtual double area() const = 0; 
    virtual ~Shape(){} 
};

class Circle : public Shape { 
public: 
    double area() const override { 
        return 3.14; 
    } 
};

// Adding a new shape doesn't require modifying Shape or Circle classes!
class Rect : public Shape { 
public: 
    double area() const override { 
        return 4.0; 
    } 
};

int main() { 
    Circle c; 
    Rect r; 
    std::cout << "Circle Area: " << c.area() << ", Rect Area: " << r.area() << "\\n"; 
    return 0; 
}
""",

"2_SOLID/3_LSP_LiskovSubstitution.cpp": """#include <iostream>

/*
 * CONCEPT: Liskov Substitution Principle (LSP) - The 'L' in SOLID
 * 
 * WHAT: Objects of a superclass should be replaceable with objects of its subclasses 
 *       without breaking the application.
 * 
 * HOW: Subclasses must strictly honor the contract established by the base class. 
 *      If a Base class guarantees a behavior (like `fly()`), a subclass cannot throw an 
 *      exception or fail to perform that behavior (like an Ostrich subclass).
 * 
 * WHY: Ensures predictability. Code that uses the Base class pointer shouldn't have to 
 *      guess if the specific subclass will crash or behave entirely differently.
 */

class Bird { 
public: 
    virtual void fly() = 0; 
    virtual ~Bird(){} 
};

class Sparrow : public Bird { 
public: 
    void fly() override { 
        std::cout << "Sparrow flies normally\\n"; 
    } 
};

// Notice we do NOT have an Ostrich class inheriting Bird, 
// because Ostrich cannot fly, which would violate LSP!

int main() { 
    Bird* b = new Sparrow(); 
    
    // We can confidently call fly() without worrying about which bird it is
    b->fly(); 
    
    delete b; 
    return 0; 
}
""",

"2_SOLID/4_ISP_InterfaceSegregation.cpp": """#include <iostream>

/*
 * CONCEPT: Interface Segregation Principle (ISP) - The 'I' in SOLID
 * 
 * WHAT: Clients should not be forced to depend on interfaces (methods) they do not use.
 * 
 * HOW: Split large, "fat" interfaces into smaller, more specific ones. 
 *      Instead of one giant `IMachine` interface with print(), scan(), and fax(), 
 *      create `IPrinter`, `IScanner`, etc.
 * 
 * WHY: If a class only needs to print, it shouldn't be forced to provide empty, 
 *      dummy implementations for scan() or fax() just to satisfy the compiler.
 */

// Specific, segregated interfaces
class IPrinter { 
public: 
    virtual void print() = 0; 
    virtual ~IPrinter(){} 
};

class IScanner { 
public: 
    virtual void scan() = 0; 
    virtual ~IScanner(){} 
};

// Only inherits what it actually uses
class SimplePrinter : public IPrinter {
public: 
    void print() override { 
        std::cout << "Printing document\\n"; 
    }
};

int main() { 
    SimplePrinter p; 
    p.print(); 
    return 0; 
}
""",

"2_SOLID/5_DIP_DependencyInversion.cpp": """#include <iostream>

/*
 * CONCEPT: Dependency Inversion Principle (DIP) - The 'D' in SOLID
 * 
 * WHAT: High-level modules should not depend on low-level modules. Both should depend on abstractions.
 *       Abstractions should not depend on details. Details should depend on abstractions.
 * 
 * HOW: Instead of passing a concrete class (like `ConsoleLogger`) into your App, pass an interface 
 *      (`ILogger`). The App relies on the interface, not the exact implementation.
 * 
 * WHY: Decouples components. You can easily swap out `ConsoleLog` for `FileLog` or `DatabaseLog` 
 *      without ever changing the `App` class code.
 */

// Abstraction
class ILogger { 
public: 
    virtual void log() = 0; 
    virtual ~ILogger(){} 
};

// Low-level detail depending on abstraction
class ConsoleLog : public ILogger { 
public: 
    void log() override { 
        std::cout << "Console Logging\\n"; 
    } 
};

// High-level module depending on abstraction, NOT on ConsoleLog directly
class App {
    ILogger& logger; 
public:
    App(ILogger& l) : logger(l) {}
    void run() { 
        logger.log(); 
    }
};

int main() { 
    ConsoleLog c; 
    App app(c); 
    app.run(); 
    return 0; 
}
""",

"3_DesignPatterns/1_Singleton.cpp": """#include <iostream>

/*
 * CONCEPT: Singleton Design Pattern
 * 
 * WHAT: A creational pattern that ensures a class has only ONE instance, and provides 
 *       a global point of access to it.
 * 
 * HOW: 
 *   1. Make the constructor `private` to prevent standard instantiation.
 *   2. Create a `static` pointer to hold the single instance.
 *   3. Provide a `static` method (like `get()`) that creates the instance if it doesn't exist, 
 *      and returns it.
 * 
 * WHY: Useful for resources where it makes no sense to have multiple copies, like a 
 *      Database Connection Pool, Logger, or Configuration Manager.
 */

class Singleton {
    static Singleton* instance;
    
    // Private constructor
    Singleton() {}
    
public:
    // Global access point
    static Singleton* get() {
        if(!instance) {
            instance = new Singleton();
        }
        return instance;
    }
    
    void doWork() { 
        std::cout << "Singleton instance working\\n"; 
    }
};

// Initialize static member
Singleton* Singleton::instance = nullptr;

int main() { 
    Singleton::get()->doWork(); 
    return 0; 
}
""",

"3_DesignPatterns/2_Factory.cpp": """#include <iostream>

/*
 * CONCEPT: Factory Method Design Pattern
 * 
 * WHAT: A creational pattern that provides an interface for creating objects, but allows 
 *       subclasses or factory classes to alter the type of objects that will be created.
 * 
 * HOW: Instead of calling `new Sedan()` directly in your main code, you call a static 
 *      method `CarFactory::makeCar()`. The factory encapsulates the `new` keyword logic.
 * 
 * WHY: Centralizes object creation. If object creation gets complex, or if you want to 
 *      decide which object to return based on conditions, you do it in ONE place (the Factory).
 */

class Car { 
public: 
    virtual void drive() = 0; 
    virtual ~Car(){} 
};

class Sedan : public Car { 
public: 
    void drive() override { 
        std::cout << "Driving Sedan\\n"; 
    } 
};

// Encapsulates object creation
class CarFactory {
public: 
    static Car* makeCar() { 
        return new Sedan(); // Could easily be swapped or contain logic
    }
};

int main() { 
    // Client code doesn't use 'new', it asks the factory
    Car* c = CarFactory::makeCar(); 
    c->drive(); 
    delete c; 
    return 0; 
}
""",

"3_DesignPatterns/3_Observer.cpp": """#include <iostream>
#include <vector>

/*
 * CONCEPT: Observer Design Pattern
 * 
 * WHAT: A behavioral pattern that defines a one-to-many dependency. When one object 
 *       (Subject) changes state, all its dependents (Observers) are notified automatically.
 * 
 * HOW: The Subject holds a list of Observer pointers. When the Subject's state changes, 
 *      it loops through the list and calls an `update()` method on each Observer.
 * 
 * WHY: Highly decouples systems. The Subject doesn't need to know anything about the Observers 
 *      other than that they implement `update()`. Excellent for event systems, UI updates, or publish/subscribe.
 */

class Observer { 
public: 
    virtual void update() = 0; 
    virtual ~Observer(){} 
};

class Subject {
    std::vector<Observer*> obs;
public:
    void add(Observer* o) { 
        obs.push_back(o); 
    }
    
    void notify() { 
        for(auto o : obs) {
            o->update(); 
        }
    }
};

class User : public Observer { 
public: 
    void update() override { 
        std::cout << "User was notified of a change!\\n"; 
    } 
};

int main() { 
    Subject s; 
    User u; 
    
    s.add(&u); 
    s.notify(); // Automatically triggers u.update()
    
    return 0; 
}
""",

"3_DesignPatterns/4_Strategy.cpp": """#include <iostream>

/*
 * CONCEPT: Strategy Design Pattern
 * 
 * WHAT: A behavioral pattern that lets you define a family of algorithms, put each of them 
 *       into a separate class, and make their objects interchangeable at runtime.
 * 
 * HOW: Create a common `Strategy` interface. Create concrete classes implementing that interface. 
 *      A `Context` object holds a pointer to a `Strategy` and uses it to execute the behavior.
 * 
 * WHY: Replaces giant `if-else` or `switch` statements for picking algorithms. You can swap 
 *      behaviors (like Sorting algorithms, or Routing methods) dynamically at runtime.
 */

class Strategy { 
public: 
    virtual void execute() = 0; 
    virtual ~Strategy(){} 
};

// Concrete Strategy A
class FastStrategy : public Strategy { 
public: 
    void execute() override { 
        std::cout << "Executing Fast Strategy Algorithm\\n"; 
    } 
};

// The Context runs the assigned strategy
class Context {
    Strategy* s;
public:
    void set(Strategy* strat) { 
        s = strat; 
    }
    void run() { 
        if(s) s->execute(); 
    }
};

int main() { 
    FastStrategy f; 
    Context c; 
    
    c.set(&f); // Swap behavior at runtime
    c.run(); 
    
    return 0; 
}
""",

"4_UML_and_Relationships/1_UML_Relationships.cpp": """#include <iostream>

/*
 * CONCEPT: UML Relationships (Aggregation vs Composition)
 * 
 * WHAT & HOW:
 *   1. Aggregation ("Has-A", Weak Relationship):
 *      - A class contains a POINTER or REFERENCE to another class.
 *      - If the parent dies, the child CAN STILL EXIST independently.
 *      - Example: Department has Teachers. If the Department closes, Teachers still exist.
 * 
 *   2. Composition ("Part-Of", Strong Relationship):
 *      - A class contains an INSTANCE of another class directly.
 *      - If the parent dies, the child DIES WITH IT.
 *      - Example: House has Rooms. If you destroy the House, the Rooms are destroyed too.
 * 
 * WHY: Crucial for managing memory and understanding the true lifecycle of objects in your system.
 */

class Teacher {};

// AGGREGATION: Department holds pointers to Teachers
class Department { 
    Teacher* t; 
}; 

class Room {};

// COMPOSITION: House physically contains the Room instance
class House { 
    Room r; 
}; 

int main() { 
    std::cout << "UML Relationships: Aggregation vs Composition\\n"; 
    return 0; 
}
""",

"4_UML_and_Relationships/2_UML_ParkingLot_CRUD.cpp": """#include <iostream>

/*
 * CONCEPT: Object-Oriented CRUD (Create, Read, Update, Delete) Basics
 * 
 * WHAT: A minimal representation of state management using a real-world entity (Parking Lot).
 * 
 * HOW: Expose simple methods (`park()`, `unpark()`) that internally update the state 
 *      of member objects (the `Spot`'s `isFree` boolean).
 * 
 * WHY: Demonstrates how Low-Level Design bridges real-world actions to internal data mutations 
 *      while hiding the direct data manipulation from the user.
 */

class Spot { 
public: 
    bool isFree = true; 
};

class ParkingLot {
    Spot spot;
public:
    // Update State -> Park
    void park() { 
        spot.isFree = false; 
        std::cout << "Vehicle Parked. Spot occupied.\\n"; 
    }
    
    // Update State -> Unpark
    void unpark() { 
        spot.isFree = true; 
        std::cout << "Vehicle Unparked. Spot freed.\\n"; 
    }
};

int main() { 
    ParkingLot p; 
    p.park(); 
    p.unpark(); 
    return 0; 
}
""",

"4_UML_and_Relationships/3_DontOvercomplicate.cpp": """#include <iostream>

/*
 * CONCEPT: KISS Principle (Keep It Simple, Stupid) & YAGNI (You Aren't Gonna Need It)
 * 
 * WHAT: Avoiding over-engineering. Do not build massive abstract hierarchies, complex 
 *       factories, or extensive observer systems if a simple class or function will suffice.
 * 
 * HOW: Write the minimal amount of code to solve the current problem. Refactor to introduce 
 *      design patterns ONLY when the codebase organically demands it due to scaling complexity.
 * 
 * WHY: Over-engineered code is harder to read, harder to debug, and slower to compile. 
 *      Simplicity is the ultimate sophistication.
 */

int main() { 
    std::cout << "KISS: Keep It Simple, Stupid. Only use patterns when necessary.\\n"; 
    return 0; 
}
"""
}

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    if os.path.exists(full_path):
        with open(full_path, "w") as f:
            f.write(content)
        print(f"Added explanatory comments to {rel_path}")

