import os

base_dir = "/home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete"

files = {
"1_OOPs/1_Abstraction.cpp": """#include <iostream>

// Abstraction: Hiding internal details and showing only functionality.
class Car {
private:
    void igniteEngine() { 
        /* hidden detail */ 
    }
public:
    void start() { 
        igniteEngine(); 
        std::cout << "Car started\\n"; 
    }
};

int main() { 
    Car c; 
    c.start(); 
    return 0; 
}
""",

"1_OOPs/2_Encapsulation.cpp": """#include <iostream>

// Encapsulation: Binding data and functions together, restricting direct access.
class BankAccount {
private:
    int balance = 0;
public:
    void deposit(int amt) { 
        if(amt > 0) {
            balance += amt; 
        }
    }
    
    int getBalance() const { 
        return balance; 
    }
};

int main() { 
    BankAccount b; 
    b.deposit(100); 
    std::cout << b.getBalance() << "\\n"; 
    return 0; 
}
""",

"1_OOPs/3_Inheritance.cpp": """#include <iostream>

// Inheritance: Reusing code from a base class.
class Animal { 
public: 
    void eat() { 
        std::cout << "Eating\\n"; 
    } 
};

class Dog : public Animal { 
public: 
    void bark() { 
        std::cout << "Barking\\n"; 
    } 
};

int main() { 
    Dog d; 
    d.eat(); 
    d.bark(); 
    return 0; 
}
""",

"1_OOPs/4_Polymorphism.cpp": """#include <iostream>

// Polymorphism: One interface, multiple implementations.
class Animal { 
public: 
    virtual void sound() { 
        std::cout << "Animal sound\\n"; 
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
    Animal* a = new Dog(); 
    a->sound(); 
    delete a; 
    return 0; 
}
""",

"1_OOPs/5_VTable_VPointer.cpp": """#include <iostream>

// VTable & VPointer mechanism
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
    b->show(); 
    delete b; 
    return 0; 
}
""",

"1_OOPs/6_Virtual_vs_PureVirtual.cpp": """#include <iostream>

class Base {
public:
    virtual void standard() { 
        std::cout << "Standard Virtual\\n"; 
    }
    
    // Pure virtual makes class Abstract
    virtual void pure() = 0; 
    
    virtual ~Base(){}
};

class Derived : public Base {
public:
    void pure() override { 
        std::cout << "Pure Implemented\\n"; 
    }
};

int main() { 
    Base* b = new Derived(); 
    b->standard(); 
    b->pure(); 
    delete b; 
    return 0; 
}
""",

"2_SOLID/1_SRP_SingleResponsibility.cpp": """#include <iostream>

// Single Responsibility: A class should have one reason to change.
class Order { 
public: 
    double price = 100.0; 
};

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

// Open/Closed: Open for extension, closed for modification.
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

class Rect : public Shape { 
public: 
    double area() const override { 
        return 4.0; 
    } 
};

int main() { 
    Circle c; 
    Rect r; 
    std::cout << c.area() << ", " << r.area() << "\\n"; 
    return 0; 
}
""",

"2_SOLID/3_LSP_LiskovSubstitution.cpp": """#include <iostream>

// Liskov Substitution: Derived types must be substitutable for base types.
class Bird { 
public: 
    virtual void fly() = 0; 
    virtual ~Bird(){} 
};

class Sparrow : public Bird { 
public: 
    void fly() override { 
        std::cout << "Sparrow flies\\n"; 
    } 
};

// Ostrich shouldn't inherit Bird if Bird forces fly().
int main() { 
    Bird* b = new Sparrow(); 
    b->fly(); 
    delete b; 
    return 0; 
}
""",

"2_SOLID/4_ISP_InterfaceSegregation.cpp": """#include <iostream>

// Interface Segregation: Clients shouldn't be forced to depend on methods they don't use.
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

class SimplePrinter : public IPrinter {
public: 
    void print() override { 
        std::cout << "Printing\\n"; 
    }
};

int main() { 
    SimplePrinter p; 
    p.print(); 
    return 0; 
}
""",

"2_SOLID/5_DIP_DependencyInversion.cpp": """#include <iostream>

// Dependency Inversion: Depend on abstractions, not concretions.
class ILogger { 
public: 
    virtual void log() = 0; 
    virtual ~ILogger(){} 
};

class ConsoleLog : public ILogger { 
public: 
    void log() override { 
        std::cout << "Console Logging\\n"; 
    } 
};

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

// Singleton: Ensure a class has only one instance.
class Singleton {
    static Singleton* instance;
    Singleton() {}
public:
    static Singleton* get() {
        if(!instance) {
            instance = new Singleton();
        }
        return instance;
    }
    
    void doWork() { 
        std::cout << "Singleton working\\n"; 
    }
};

Singleton* Singleton::instance = nullptr;

int main() { 
    Singleton::get()->doWork(); 
    return 0; 
}
""",

"3_DesignPatterns/2_Factory.cpp": """#include <iostream>

// Factory: Create objects without specifying exact classes.
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

class CarFactory {
public: 
    static Car* makeCar() { 
        return new Sedan(); 
    }
};

int main() { 
    Car* c = CarFactory::makeCar(); 
    c->drive(); 
    delete c; 
    return 0; 
}
""",

"3_DesignPatterns/3_Observer.cpp": """#include <iostream>
#include <vector>

// Observer: Notify dependents when state changes.
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
        for(auto o : obs) o->update(); 
    }
};

class User : public Observer { 
public: 
    void update() override { 
        std::cout << "Notified!\\n"; 
    } 
};

int main() { 
    Subject s; 
    User u; 
    s.add(&u); 
    s.notify(); 
    return 0; 
}
""",

"3_DesignPatterns/4_Strategy.cpp": """#include <iostream>

// Strategy: Encapsulate algorithms to make them interchangeable.
class Strategy { 
public: 
    virtual void execute() = 0; 
    virtual ~Strategy(){} 
};

class FastStrategy : public Strategy { 
public: 
    void execute() override { 
        std::cout << "Fast Strategy\\n"; 
    } 
};

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
    c.set(&f); 
    c.run(); 
    return 0; 
}
""",

"4_UML_and_Relationships/1_UML_Relationships.cpp": """#include <iostream>

// Aggregation: "has-a", child can exist independently (Department -> Teachers)
// Composition: "part-of", child dies with parent (House -> Rooms)
class Teacher {};
class Department { 
    Teacher* t; 
}; // Aggregation

class Room {};
class House { 
    Room r; 
}; // Composition

int main() { 
    std::cout << "UML Relationships: Aggregation vs Composition\\n"; 
    return 0; 
}
""",

"4_UML_and_Relationships/2_UML_ParkingLot_CRUD.cpp": """#include <iostream>

// Simple Parking Lot
class Spot { 
public: 
    bool isFree = true; 
};

class ParkingLot {
    Spot spot;
public:
    void park() { 
        spot.isFree = false; 
        std::cout << "Parked\\n"; 
    }
    void unpark() { 
        spot.isFree = true; 
        std::cout << "Unparked\\n"; 
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

// Keep it simple stupid (KISS). Don't overengineer.
int main() { 
    std::cout << "KISS: Keep It Simple, Stupid.\\n"; 
    return 0; 
}
"""
}

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    if os.path.exists(full_path):
        with open(full_path, "w") as f:
            f.write(content)
        print(f"Formatted {rel_path}")

