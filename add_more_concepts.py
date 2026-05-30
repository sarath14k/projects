import os

base_dir = "/home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete"

files = {
"5_Modern_CPP/4_RuleOfFive.cpp": """// To compile and run: cd {dir} && g++ -std=c++17 {basename} -o {no_ext} && ./{no_ext}
#include <iostream>
#include <utility>

/*
 * CONCEPT: Rule of Five (C++11)
 * 
 * WHAT: If a class defines one of the following, it should probably define all five:
 *       1. Destructor
 *       2. Copy Constructor
 *       3. Copy Assignment Operator
 *       4. Move Constructor
 *       5. Move Assignment Operator
 * 
 * HOW: Explicitly define them to manage dynamic resources (like raw pointers) safely, 
 *      or use `= default` / `= delete` to enforce semantics.
 * 
 * WHY: Prevents shallow copy bugs, double-free memory corruption, and memory leaks 
 *      when dealing with classes that manually manage resources on the heap.
 */

class Resource {
    int* data;
public:
    // 1. Constructor
    Resource(int val) : data(new int(val)) { std::cout << "Constructor\\n"; }
    
    // 2. Destructor
    ~Resource() { delete data; std::cout << "Destructor\\n"; }
    
    // 3. Copy Constructor (Deep Copy)
    Resource(const Resource& other) : data(new int(*other.data)) { std::cout << "Copy Constructor\\n"; }
    
    // 4. Copy Assignment (Deep Copy)
    Resource& operator=(const Resource& other) {
        if (this != &other) { delete data; data = new int(*other.data); }
        std::cout << "Copy Assignment\\n";
        return *this;
    }
    
    // 5. Move Constructor (Steal Resource)
    Resource(Resource&& other) noexcept : data(other.data) {
        other.data = nullptr;
        std::cout << "Move Constructor\\n";
    }
    
    // 6. Move Assignment (Steal Resource)
    Resource& operator=(Resource&& other) noexcept {
        if (this != &other) { delete data; data = other.data; other.data = nullptr; }
        std::cout << "Move Assignment\\n";
        return *this;
    }
};

int main() {
    std::cout << "--- Creating a ---\\n";
    Resource a(10);           
    
    std::cout << "--- Copying a to b ---\\n";
    Resource b = a;           
    
    std::cout << "--- Assigning a to c ---\\n";
    Resource c(20);           
    c = a;                    
    
    std::cout << "--- Moving a to d ---\\n";
    Resource d = std::move(a);
    
    std::cout << "--- Exiting (Destructors) ---\\n";
    return 0;
}
""",

"6_Concurrency/1_Threads_Mutex.cpp": """// To compile and run: cd {dir} && g++ -std=c++17 -pthread {basename} -o {no_ext} && ./{no_ext}
#include <iostream>
#include <thread>
#include <mutex>

/*
 * CONCEPT: Multithreading & Mutex
 * 
 * WHAT: Running multiple threads of execution concurrently to utilize multi-core processors. 
 *       Mutex (Mutual Exclusion) ensures that multiple threads do not modify shared data simultaneously.
 * 
 * HOW: Use `std::thread` to spawn threads. Use `std::mutex` and `std::lock_guard` to lock critical sections.
 * 
 * WHY: Threads improve performance via parallelism. Mutexes prevent "race conditions" where thread A 
 *      and thread B try to overwrite the same memory address at the exact same time, causing corruption.
 */

std::mutex mtx;
int counter = 0;

void incrementCounter(int id) {
    // lock_guard automatically locks the mutex, and unlocks it when it goes out of scope (RAII)
    std::lock_guard<std::mutex> lock(mtx);
    
    counter++;
    std::cout << "Thread " << id << " incremented counter to " << counter << "\\n";
}

int main() {
    // Spawn two threads executing the same function
    std::thread t1(incrementCounter, 1);
    std::thread t2(incrementCounter, 2);
    
    // Wait for threads to finish before main exits
    t1.join();
    t2.join();
    
    std::cout << "Final Counter: " << counter << "\\n";
    return 0;
}
""",

"3_DesignPatterns/5_Builder.cpp": """// To compile and run: cd {dir} && g++ -std=c++17 {basename} -o {no_ext} && ./{no_ext}
#include <iostream>
#include <string>

/*
 * CONCEPT: Builder Design Pattern
 * 
 * WHAT: A creational pattern used to construct a complex object step by step.
 * 
 * HOW: Separate the construction of a complex object from its representation. You chain methods 
 *      returning `*this` (or reference) to slowly build the object before finally returning it.
 * 
 * WHY: Solves the "Telescoping Constructor" anti-pattern (a constructor with 10+ confusing parameters). 
 *      It makes object instantiation highly readable and allows for optional parameters easily.
 */

class Computer {
public:
    std::string cpu, ram, storage;
    void show() { std::cout << "PC: " << cpu << ", " << ram << ", " << storage << "\\n"; }
};

class ComputerBuilder {
    Computer pc;
public:
    ComputerBuilder& setCPU(std::string cpu) { pc.cpu = cpu; return *this; }
    ComputerBuilder& setRAM(std::string ram) { pc.ram = ram; return *this; }
    ComputerBuilder& setStorage(std::string storage) { pc.storage = storage; return *this; }
    
    Computer build() { return pc; }
};

int main() {
    // Highly readable chaining to build a complex object
    Computer gamingRig = ComputerBuilder()
                            .setCPU("Intel i9")
                            .setRAM("32GB")
                            .setStorage("2TB NVMe")
                            .build();
                            
    gamingRig.show();
    return 0;
}
""",

"7_Templates/1_Templates.cpp": """// To compile and run: cd {dir} && g++ -std=c++17 {basename} -o {no_ext} && ./{no_ext}
#include <iostream>
#include <string>

/*
 * CONCEPT: Templates (Generic Programming)
 * 
 * WHAT: A feature that allows you to write functions or classes that work with any data type.
 * 
 * HOW: Use the `template <typename T>` declaration. The compiler will generate the specific 
 *      version of the function/class at compile-time when you call it with a specific type.
 * 
 * WHY: Prevents code duplication. Instead of writing `int add(int, int)` and `double add(double, double)`, 
 *      you write one generic template that can handle `int`, `double`, `float`, or custom objects.
 */

// Generic Function Template
template <typename T>
T add(T a, T b) {
    return a + b;
}

// Generic Class Template
template <typename T>
class Box {
    T value;
public:
    Box(T v) : value(v) {}
    T getValue() { return value; }
};

int main() {
    // Compiler generates int version
    std::cout << "Int Add: " << add(5, 10) << "\\n";
    
    // Compiler generates double version
    std::cout << "Double Add: " << add(5.5, 2.2) << "\\n";
    
    Box<std::string> stringBox("Templates are powerful!");
    std::cout << "Box holds: " << stringBox.getValue() << "\\n";
    
    return 0;
}
"""
}

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    dir_path = os.path.dirname(full_path)
    basename = os.path.basename(full_path)
    no_ext = os.path.splitext(basename)[0]
    
    final_content = content.format(dir=dir_path, basename=basename, no_ext=no_ext)
    
    with open(full_path, "w") as f:
        f.write(final_content)
    print(f"Created {rel_path}")
