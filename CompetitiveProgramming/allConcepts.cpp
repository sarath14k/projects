#include <iostream>          // For standard I/O operations
#include <vector>           // For std::vector
#include <array>            // For std::array
#include <list>             // For std::list
#include <map>              // For std::map
#include <set>              // For std::set
#include <unordered_map>    // For std::unordered_map
#include <algorithm>        // For std::sort, std::for_each
#include <string>           // For std::string
#include <cstring>          // For C-style strings
#include <memory>           // For smart pointers
#include <thread>           // For multithreading
#include <mutex>            // For mutex
#include <condition_variable> // For condition_variable
#include <chrono>           // For time functions
#include <future>           // For futures and promises
#include <optional>         // For std::optional
#include <variant>          // For std::variant
#include <any>              // For std::any
#include <regex>            // For regular expressions
#include <bitset>           // For std::bitset
#include <tuple>            // For std::tuple
#include <cmath>            // For mathematical functions
#include <fstream>          // For file operations
#include <filesystem>       // For filesystem operations
#include <queue>

void demonstrateSFINAE();       // Forward declaration
void demonstrateConcepts();     // Forward declaration
template <typename T>
void demonstrateForward(T&& arg); // Forward declaration


// 1. Basic I/O
void demonstrateIO() {
    std::cout << "Hello, World!" << std::endl; // Output a greeting
}

// 2. Variables and Data Types
void demonstrateVariables() {
    int a = 5;                    // Integer variable
    double b = 3.14;             // Double variable
    char c = 'A';                // Char variable
    std::string str = "Hello";   // String variable
    std::cout << "Integer: " << a << ", Double: " << b << ", Char: " << c << ", String: " << str << std::endl; // Output variables
}

// 3. Control Structures (if-else)
void demonstrateIfElse() {
    int num = 10; // Example number
    if (num > 0) {
        std::cout << "Positive number" << std::endl; // Output if positive
    } else {
        std::cout << "Negative number or zero" << std::endl; // Output otherwise
    }
}

// 4. Loops (for loop)
void demonstrateForLoop() {
    for (int i = 0; i < 5; ++i) {
        std::cout << "Loop iteration: " << i << std::endl; // Output current iteration
    }
}

// 5. Loops (while loop)
void demonstrateWhileLoop() {
    int count = 0; // Initialize count
    while (count < 5) {
        std::cout << "While loop count: " << count << std::endl; // Output current count
        ++count; // Increment count
    }
}

// 6. Functions
int add(int x, int y) { // Function to add two numbers
    return x + y; // Return sum
}

// 7. Function Overloading
double add(double x, double y) { // Overloaded function for double
    return x + y; // Return sum
}

// 8. Default Arguments
void printMessage(const std::string& message = "Default message") { // Function with default argument
    std::cout << message << std::endl; // Output message
}

// 9. Inline Functions
inline int square(int x) { // Inline function to calculate square
    return x * x; // Return square
}

// 10. Pointers
void demonstratePointers() {
    int value = 42; // Integer variable
    int* ptr = &value; // Pointer to value
    std::cout << "Value: " << *ptr << std::endl; // Output value through pointer
}

// 11. References
void demonstrateReferences() {
    int a = 10; // Integer variable
    int& ref = a; // Reference to a
    ref = 20; // Change value through reference
    std::cout << "Changed value: " << a << std::endl; // Output changed value
}

// 12. Arrays
void demonstrateArrays() {
    int arr[3] = {1, 2, 3}; // Declare array
    for (int i = 0; i < 3; ++i) {
        std::cout << "Array element: " << arr[i] << std::endl; // Output array elements
    }
}

// 13. std::vector
void demonstrateVector() {
    std::vector<int> vec = {1, 2, 3}; // Create vector
    vec.push_back(4); // Add element to vector
    std::cout << "Vector elements: ";
    for (const auto& elem : vec) {
        std::cout << elem << " "; // Output vector elements
    }
    std::cout << std::endl;
}

// 14. std::array
void demonstrateStdArray() {
    std::array<int, 3> arr = {4, 5, 6}; // Create std::array
    std::cout << "std::array elements: ";
    for (const auto& elem : arr) {
        std::cout << elem << " "; // Output array elements
    }
    std::cout << std::endl;
}

// 15. std::list
void demonstrateList() {
    std::list<int> myList = {1, 2, 3}; // Create list
    myList.push_back(4); // Add to list
    std::cout << "List elements: ";
    for (const auto& elem : myList) {
        std::cout << elem << " "; // Output list elements
    }
    std::cout << std::endl;
}

// 16. std::set
void demonstrateSet() {
    std::set<int> mySet = {3, 1, 2}; // Create set
    mySet.insert(4); // Insert into set
    std::cout << "Set elements: ";
    for (const auto& elem : mySet) {
        std::cout << elem << " "; // Output set elements
    }
    std::cout << std::endl;
}

// 17. std::map
void demonstrateMap() {
    std::map<std::string, int> myMap; // Create map
    myMap["one"] = 1; // Insert key-value pair
    myMap["two"] = 2; // Insert key-value pair
    std::cout << "Map elements: ";
    for (const auto& pair : myMap) {
        std::cout << pair.first << ": " << pair.second << ", "; // Output key-value pairs
    }
    std::cout << std::endl;
}

// 18. std::unordered_map
void demonstrateUnorderedMap() {
    std::unordered_map<std::string, int> myMap; // Create unordered map
    myMap["one"] = 1; // Insert key-value pair
    myMap["two"] = 2; // Insert key-value pair
    std::cout << "Unordered Map elements: ";
    for (const auto& pair : myMap) {
        std::cout << pair.first << ": " << pair.second << ", "; // Output key-value pairs
    }
    std::cout << std::endl;
}

// 19. std::deque
void demonstrateDeque() {
    std::deque<int> myDeque = {1, 2, 3}; // Create deque
    myDeque.push_back(4); // Add to back
    std::cout << "Deque elements: ";
    for (const auto& elem : myDeque) {
        std::cout << elem << " "; // Output deque elements
    }
    std::cout << std::endl;
}

// 20. std::stack
void demonstrateStack() {
    std::stack<int> myStack; // Create stack
    myStack.push(1); // Push to stack
    myStack.push(2); // Push to stack
    std::cout << "Stack top: " << myStack.top() << std::endl; // Output top element
    myStack.pop(); // Pop from stack
}

// 21. std::queue
void demonstrateQueue() {
    std::queue<int> myQueue; // Create queue
    myQueue.push(1); // Push to queue
    std::cout << "Queue front: " << myQueue.front() << std::endl; // Display front element
}

// 22. std::priority_queue
void demonstratePriorityQueue() {
    std::priority_queue<int> myPQ; // Create priority queue
    myPQ.push(1); // Push to priority queue
    std::cout << "Priority Queue top: " << myPQ.top() << std::endl; // Display top element
}


// 23. Lambda Expressions
void demonstrateLambda() {
    auto square = [](int x) { return x * x; }; // Define lambda function
    std::cout << "Square of 5: " << square(5) << std::endl; // Output square
}

// 24. std::function
void demonstrateStdFunction() {
    std::function<int(int, int)> addFunc = [](int x, int y) { return x + y; }; // Use std::function
    std::cout << "Sum: " << addFunc(2, 3) << std::endl; // Output sum
}

// 25. Exception Handling
void demonstrateExceptionHandling() {
    try {
        throw std::runtime_error("Error occurred!"); // Throw exception
    } catch (const std::runtime_error& e) {
        std::cout << "Caught exception: " << e.what() << std::endl; // Catch and output exception
    }
}

// 26. Smart Pointers (std::unique_ptr)
void demonstrateUniquePtr() {
    std::unique_ptr<int> uptr = std::make_unique<int>(42); // Create unique_ptr
    std::cout << "Unique Pointer Value: " << *uptr << std::endl; // Output value
}

// 27. Smart Pointers (std::shared_ptr)
void demonstrateSharedPtr() {
    std::shared_ptr<int> sptr = std::make_shared<int>(42); // Create shared_ptr
    std::cout << "Shared Pointer Value: " << *sptr << std::endl; // Output value
}

// 28. Type Casting (static_cast)
void demonstrateStaticCast() {
    double pi = 3.14; // Double variable
    int intPi = static_cast<int>(pi); // Cast to int
    std::cout << "Static Cast: " << intPi << std::endl; // Output casted value
}

// 29. Type Casting (dynamic_cast)
class Base { virtual void foo() {} }; // Base class with virtual function
class Derived : public Base {}; // Derived class

void demonstrateDynamicCast() {
    Base* b = new Derived; // Create base pointer to derived object
    Derived* d = dynamic_cast<Derived*>(b); // Safe downcasting
    if (d) {
        std::cout << "Dynamic cast successful!" << std::endl; // Successful cast
    }
    delete b; // Clean up
}

// 30. Type Casting (reinterpret_cast)
void demonstrateReinterpretCast() {
    int a = 65; // Integer variable
    char* ptr = reinterpret_cast<char*>(&a); // Reinterpret cast
    std::cout << "Reinterpret Cast: " << *ptr << std::endl; // Output reinterpret cast value
}

// 31. std::string and C-style Strings
void demonstrateCString() {
    const char* cstr = "Hello"; // C-style string
    std::string str(cstr); // Convert to std::string
    std::cout << "C-style string: " << cstr << ", std::string: " << str << std::endl; // Output both
}

// 32. std::string Methods
void demonstrateStringMethods() {
    std::string str = "Hello, World!"; // Create string
    std::cout << "Length: " << str.length() << std::endl; // Output length
    std::cout << "Substring: " << str.substr(0, 5) << std::endl; // Output substring
}

// 33. std::bitset
void demonstrateBitset() {
    std::bitset<8> bits(42); // Create bitset
    std::cout << "Bitset: " << bits << std::endl; // Output bitset
}

// 34. std::tuple
void demonstrateTuple() {
    std::tuple<int, double, std::string> tup = std::make_tuple(1, 2.5, "Tuple"); // Create tuple
    std::cout << "Tuple: (" << std::get<0>(tup) << ", " << std::get<1>(tup) << ", " << std::get<2>(tup) << ")" << std::endl; // Output tuple elements
}

// 35. std::optional
void demonstrateOptional() {
    std::optional<int> opt; // Create optional
    if (!opt) {
        std::cout << "Optional has no value." << std::endl; // Output if no value
    }
    opt = 10; // Assign value
    std::cout << "Optional value: " << *opt << std::endl; // Output value
}

// 36. std::variant
void demonstrateVariant() {
    std::variant<int, std::string> var; // Create variant
    var = 42; // Assign int
    std::visit([](auto&& arg) { std::cout << "Variant holds: " << arg << std::endl; }, var); // Visit variant
}

// 37. std::any
void demonstrateAny() {
    std::any a = 10; // Create any
    std::cout << "Any holds: " << std::any_cast<int>(a) << std::endl; // Cast any to int
}

// 38. Regular Expressions
void demonstrateRegex() {
    std::regex r("\\d+"); // Create regex
    std::string s = "123";
    if (std::regex_match(s, r)) { // Match regex
        std::cout << "Regex matched!" << std::endl; // Output message
    }
}

// 39. std::chrono
void demonstrateChrono() {
    auto start = std::chrono::high_resolution_clock::now(); // Start time
    std::this_thread::sleep_for(std::chrono::milliseconds(100)); // Simulate work
    auto end = std::chrono::high_resolution_clock::now(); // End time
    std::chrono::duration<double, std::milli> duration = end - start; // Calculate duration
    std::cout << "Duration: " << duration.count() << " ms" << std::endl; // Output duration
}

// 40. std::thread
void demonstrateThread() {
    std::thread t([]() { std::cout << "Thread is running!" << std::endl; }); // Create thread
    t.join(); // Wait for thread to finish
}

// 41. std::mutex
void demonstrateMutex() {
    std::mutex mtx; // Create mutex
    std::lock_guard<std::mutex> lock(mtx); // Lock mutex
    std::cout << "Mutex is locked." << std::endl; // Output message
}

// 42. std::condition_variable
void demonstrateConditionVariable() {
    std::mutex mtx; // Create mutex
    std::condition_variable cv; // Create condition variable
    std::thread t([&]() {
        std::unique_lock<std::mutex> lock(mtx); // Lock mutex
        cv.wait(lock); // Wait for condition variable
        std::cout << "Condition variable notified." << std::endl; // Output message
    });
    cv.notify_one(); // Notify one thread
    t.join(); // Wait for thread to finish
}

// 43. std::atomic
void demonstrateAtomic() {
    std::atomic<int> atomicInt(0); // Create atomic variable
    atomicInt++; // Increment atomic variable
    std::cout << "Atomic value: " << atomicInt.load() << std::endl; // Output value
}

// 44. std::filesystem
void demonstrateFilesystem() {
    std::filesystem::path p = "example.txt"; // Create file path
    std::ofstream ofs(p); // Create output file stream
    ofs << "Hello, Filesystem!"; // Write to file
    ofs.close(); // Close file
    std::cout << "File created: " << p << std::endl; // Output message
}

// 45. File Input/Output
void demonstrateFileIO() {
    std::ofstream outFile("output.txt"); // Create output file
    outFile << "Hello, File!" << std::endl; // Write to file
    outFile.close(); // Close output file

    std::ifstream inFile("output.txt"); // Open input file
    std::string line;
    while (std::getline(inFile, line)) { // Read file line by line
        std::cout << line << std::endl; // Output each line
    }
    inFile.close(); // Close input file
}

// 46. Command Line Arguments
void demonstrateCommandLineArguments(int argc, char* argv[]) {
    std::cout << "Command line arguments: " << std::endl; // Output message
    for (int i = 0; i < argc; ++i) {
        std::cout << argv[i] << std::endl; // Output each argument
    }
}

// 47. Enum Classes
enum class Color { Red, Green, Blue }; // Define enum class

void demonstrateEnumClass() {
    Color color = Color::Red; // Use enum class
    if (color == Color::Red) {
        std::cout << "Color is Red!" << std::endl; // Output message
    }
}

// 48. Namespaces
namespace MyNamespace {
    void myFunction() {
        std::cout << "Hello from MyNamespace!" << std::endl; // Output message
    }
}

void demonstrateNamespace() {
    MyNamespace::myFunction(); // Call function from namespace
}

// 49. Templates
template <typename T>
T addTemplate(T a, T b) { // Template function
    return a + b; // Return sum
}

void demonstrateTemplates() {
    std::cout << "Template add: " << addTemplate(2, 3) << std::endl; // Call template with integers
    std::cout << "Template add: " << addTemplate(2.5, 3.5) << std::endl; // Call template with doubles
}

// 50. Template Specialization
template <>
std::string addTemplate<std::string>(std::string a, std::string b) { // Specialized template
    return a + " " + b; // Concatenate strings
}

void demonstrateTemplateSpecialization() {
    std::cout << "Specialized Template add: " << addTemplate<std::string>("Hello", "World") << std::endl; // Call specialized template
}

// 51. Static Variables
void demonstrateStaticVariable() {
    static int count = 0; // Static variable
    count++; // Increment count
    std::cout << "Static variable count: " << count << std::endl; // Output count
}

// 52. Dynamic Memory Allocation
void demonstrateDynamicMemory() {
    int* arr = new int[5]; // Allocate array
    for (int i = 0; i < 5; ++i) {
        arr[i] = i; // Initialize array
    }
    std::cout << "Dynamic array elements: ";
    for (int i = 0; i < 5; ++i) {
        std::cout << arr[i] << " "; // Output array elements
    }
    delete[] arr; // Free allocated memory
    std::cout << std::endl;
}

// 53. Function Pointers
void myFunction() {
    std::cout << "Function pointer called!" << std::endl; // Output message
}

void demonstrateFunctionPointer() {
    void (*funcPtr)() = &myFunction; // Function pointer
    funcPtr(); // Call function through pointer
}

// 54. Array of Pointers
void demonstrateArrayOfPointers() {
    int value1 = 10, value2 = 20; // Create variables
    int* arr[] = { &value1, &value2 }; // Array of pointers
    std::cout << "Values: " << *arr[0] << ", " << *arr[1] << std::endl; // Output values
}

// 55. Structs
struct Point {
    int x, y; // Struct members
};

void demonstrateStructs() {
    Point p = {1, 2}; // Create struct
    std::cout << "Point: (" << p.x << ", " << p.y << ")" << std::endl; // Output point
}

// 56. Unions
union Data {
    int intValue; // Union member
    float floatValue; // Union member
};

void demonstrateUnion() {
    Data data; // Create union
    data.intValue = 42; // Assign int
    std::cout << "Union intValue: " << data.intValue << std::endl; // Output int value
}

// 57. std::copy
void demonstrateCopy() {
    int src[] = {1, 2, 3}; // Source array
    int dest[3]; // Destination array
    std::copy(std::begin(src), std::end(src), dest); // Copy array
    std::cout << "Copied array: ";
    for (int i : dest) {
        std::cout << i << " "; // Output copied array
    }
    std::cout << std::endl;
}

// 58. std::for_each
void demonstrateForEach() {
    std::vector<int> vec = {1, 2, 3}; // Create vector
    std::cout << "For Each output: ";
    std::for_each(vec.begin(), vec.end(), [](int n) { std::cout << n << " "; }); // Use for_each with lambda
    std::cout << std::endl;
}

// 59. std::find
void demonstrateFind() {
    std::vector<int> vec = {1, 2, 3}; // Create vector
    auto it = std::find(vec.begin(), vec.end(), 2); // Find element
    if (it != vec.end()) {
        std::cout << "Found: " << *it << std::endl; // Output found element
    }
}

// 60. std::sort
void demonstrateSort() {
    std::vector<int> vec = {3, 1, 2}; // Create vector
    std::sort(vec.begin(), vec.end()); // Sort vector
    std::cout << "Sorted vector: ";
    for (int n : vec) {
        std::cout << n << " "; // Output sorted vector
    }
    std::cout << std::endl;
}

// 61. std::reverse
void demonstrateReverse() {
    std::vector<int> vec = {1, 2, 3}; // Create vector
    std::reverse(vec.begin(), vec.end()); // Reverse vector
    std::cout << "Reversed vector: ";
    for (int n : vec) {
        std::cout << n << " "; // Output reversed vector
    }
    std::cout << std::endl;
}

// 62. std::accumulate
#include <numeric> // For std::accumulate

void demonstrateAccumulate() {
    std::vector<int> vec = {1, 2, 3}; // Create vector
    int sum = std::accumulate(vec.begin(), vec.end(), 0); // Calculate sum
    std::cout << "Sum: " << sum << std::endl; // Output sum
}

// 63. std::transform
void demonstrateTransform() {
    std::vector<int> vec = {1, 2, 3}; // Create vector
    std::vector<int> squares(vec.size()); // Create vector for squares
    std::transform(vec.begin(), vec.end(), squares.begin(), [](int n) { return n * n; }); // Transform vector
    std::cout << "Squares: ";
    for (int n : squares) {
        std::cout << n << " "; // Output squares
    }
    std::cout << std::endl;
}

// 64. std::find_if
void demonstrateFindIf() {
    std::vector<int> vec = {1, 2, 3}; // Create vector
    auto it = std::find_if(vec.begin(), vec.end(), [](int n) { return n > 2; }); // Find element greater than 2
    if (it != vec.end()) {
        std::cout << "Found: " << *it << std::endl; // Output found element
    }
}

// 65. std::remove_if
void demonstrateRemoveIf() {
    std::vector<int> vec = {1, 2, 3, 4}; // Create vector
    vec.erase(std::remove_if(vec.begin(), vec.end(), [](int n) { return n % 2 == 0; }), vec.end()); // Remove even numbers
    std::cout << "After remove_if: ";
    for (int n : vec) {
        std::cout << n << " "; // Output modified vector
    }
    std::cout << std::endl;
}

// 66. std::shuffle
#include <random> // For std::shuffle

void demonstrateShuffle() {
    std::vector<int> vec = {1, 2, 3, 4, 5}; // Create vector
    std::shuffle(vec.begin(), vec.end(), std::mt19937{std::random_device{}()}); // Shuffle vector
    std::cout << "Shuffled vector: ";
    for (int n : vec) {
        std::cout << n << " "; // Output shuffled vector
    }
    std::cout << std::endl;
}

// 67. std::accumulate with custom operation
void demonstrateAccumulateCustom() {
    std::vector<int> vec = {1, 2, 3}; // Create vector
    int product = std::accumulate(vec.begin(), vec.end(), 1, std::multiplies<int>()); // Calculate product
    std::cout << "Product: " << product << std::endl; // Output product
}

// 68. std::map with lambda
void demonstrateMapLambda() {
    std::map<std::string, int> myMap = {{"one", 1}, {"two", 2}}; // Create map
    std::for_each(myMap.begin(), myMap.end(), [](const std::pair<std::string, int>& pair) {
        std::cout << pair.first << ": " << pair.second << std::endl; // Output map elements
    });
}

// 69. std::set with custom comparator
struct Compare {
    bool operator()(const int& a, const int& b) const {
        return a > b; // Descending order
    }
};

void demonstrateSetCustomComparator() {
    std::set<int, Compare> mySet = {3, 1, 2}; // Create set with custom comparator
    std::cout << "Set elements in descending order: ";
    for (const auto& elem : mySet) {
        std::cout << elem << " "; // Output set elements
    }
    std::cout << std::endl;
}

// 70. std::condition_variable with mutex
void demonstrateConditionVariableMutex() {
    std::mutex mtx; // Create mutex
    std::condition_variable cv; // Create condition variable
    bool ready = false; // Condition variable state

    std::thread worker([&]() {
        std::unique_lock<std::mutex> lock(mtx); // Lock mutex
        cv.wait(lock, [&ready] { return ready; }); // Wait for condition
        std::cout << "Worker finished!" << std::endl; // Output message
    });

    std::this_thread::sleep_for(std::chrono::seconds(1)); // Simulate work
    {
        std::lock_guard<std::mutex> lock(mtx); // Lock mutex
        ready = true; // Update condition variable state
    }
    cv.notify_one(); // Notify worker
    worker.join(); // Wait for worker to finish
}

// 71. std::shared_ptr with custom deleter
void demonstrateSharedPtrCustomDeleter() {
    auto sptr = std::shared_ptr<int>(new int(42), [](int* p) {
        std::cout << "Custom deleter called!" << std::endl; // Custom deleter
        delete p; // Free memory
    });
    std::cout << "Shared Pointer Value: " << *sptr << std::endl; // Output value
}

// 72. std::weak_ptr
void demonstrateWeakPtr() {
    std::shared_ptr<int> sptr = std::make_shared<int>(42); // Create shared_ptr
    std::weak_ptr<int> wptr = sptr; // Create weak_ptr from shared_ptr
    std::cout << "Weak Pointer Value: " << *wptr.lock() << std::endl; // Access value
}

// 73. std::array
void demonstrateArray() {
    std::array<int, 3> arr = {1, 2, 3}; // Create std::array
    std::cout << "std::array elements: ";
    for (const auto& elem : arr) {
        std::cout << elem << " "; // Output elements
    }
    std::cout << std::endl;
}

// 74. std::forward
template <typename T>
void demonstrateForward(T&& arg) {
    auto&& fwd = std::forward<T>(arg); // Perfect forwarding
    std::cout << "Forwarded value: " << fwd << std::endl; // Output value
}

// 75. std::move
void demonstrateMove() {
    std::string str = "Hello"; // Create string
    std::string movedStr = std::move(str); // Move string
    std::cout << "Moved string: " << movedStr << std::endl; // Output moved string
}

// 76. std::vector with custom allocator
template <typename T>
class CustomAllocator {
public:
    using value_type = T;
    CustomAllocator() = default;
    template <typename U> CustomAllocator(const CustomAllocator<U>&) {}
    T* allocate(std::size_t n) {
        return static_cast<T*>(::operator new(n * sizeof(T))); // Allocate memory
    }
    void deallocate(T* p, std::size_t) {
        ::operator delete(p); // Deallocate memory
    }
};

void demonstrateVectorCustomAllocator() {
    std::vector<int, CustomAllocator<int>> vec; // Create vector with custom allocator
    vec.push_back(1); // Add element
    std::cout << "Custom Allocator Vector: " << vec[0] << std::endl; // Output element
}

// 77. std::move with std::vector
void demonstrateMoveVector() {
    std::vector<int> vec = {1, 2, 3}; // Create vector
    std::vector<int> movedVec = std::move(vec); // Move vector
    std::cout << "Moved Vector Size: " << movedVec.size() << std::endl; // Output size
}

// 78. std::initializer_list
void demonstrateInitializerList() {
    std::initializer_list<int> il = {1, 2, 3}; // Create initializer list
    std::cout << "Initializer List: ";
    for (int n : il) {
        std::cout << n << " "; // Output elements
    }
    std::cout << std::endl;
}

// 79. std::variant with custom visitor
struct VariantVisitor {
    void operator()(int& n) { std::cout << "Integer: " << n << std::endl; } // Visitor for int
    void operator()(const std::string& str) { std::cout << "String: " << str << std::endl; } // Visitor for string
};

void demonstrateVariantVisitor() {
    std::variant<int, std::string> var = 42; // Create variant
    std::visit(VariantVisitor{}, var); // Visit variant with custom visitor
}

// 80. std::optional with value_or
void demonstrateOptionalValueOr() {
    std::optional<int> opt; // Create optional
    std::cout << "Optional value: " << opt.value_or(0) << std::endl; // Output default value
    opt = 10; // Assign value
    std::cout << "Optional value: " << opt.value_or(0) << std::endl; // Output value
}

// 81. std::make_unique and std::make_shared
void demonstrateMakeUniqueAndMakeShared() {
    auto uniquePtr = std::make_unique<int>(42); // Create unique_ptr
    auto sharedPtr = std::make_shared<int>(42); // Create shared_ptr
    std::cout << "Unique Pointer Value: " << *uniquePtr << ", Shared Pointer Value: " << *sharedPtr << std::endl; // Output values
}

// 82. std::aligned_storage
void demonstrateAlignedStorage() {
    std::aligned_storage<sizeof(int), alignof(int)>::type storage; // Create aligned storage
    new(&storage) int(42); // Construct int in aligned storage
    std::cout << "Aligned Storage Value: " << *reinterpret_cast<int*>(&storage) << std::endl; // Output value
}

// 83. std::variant with lambda
void demonstrateVariantLambda() {
    std::variant<int, double> var = 3.14; // Create variant
    std::visit([](auto&& arg) { std::cout << "Variant holds: " << arg << std::endl; }, var); // Visit variant with lambda
}

// 84. std::condition_variable with lambda
void demonstrateConditionVariableLambda() {
    std::mutex mtx; // Create mutex
    std::condition_variable cv; // Create condition variable
    bool ready = false; // Condition variable state

    std::thread worker([&]() {
        std::unique_lock<std::mutex> lock(mtx); // Lock mutex
        cv.wait(lock, [&ready] { return ready; }); // Wait for condition
        std::cout << "Worker finished!" << std::endl; // Output message
    });

    std::this_thread::sleep_for(std::chrono::seconds(1)); // Simulate work
    {
        std::lock_guard<std::mutex> lock(mtx); // Lock mutex
        ready = true; // Update condition variable state
    }
    cv.notify_one(); // Notify worker
    worker.join(); // Wait for worker to finish
}

// 85. std::shared_ptr with custom deleter lambda
void demonstrateSharedPtrCustomDeleterLambda() {
    auto sptr = std::shared_ptr<int>(new int(42), [](int* p) {
        std::cout << "Custom deleter lambda called!" << std::endl; // Custom deleter
        delete p; // Free memory
    });
    std::cout << "Shared Pointer Value: " << *sptr << std::endl; // Output value
}

// 86. std::weak_ptr with custom deleter
void demonstrateWeakPtrCustomDeleter() {
    std::shared_ptr<int> sptr = std::make_shared<int>(42); // Create shared_ptr
    std::weak_ptr<int> wptr(sptr); // Create weak_ptr from shared_ptr
    if (auto locked = wptr.lock()) {
        std::cout << "Weak Pointer Value: " << *locked << std::endl; // Access value
    }
}

// 87. std::array with custom allocator
void demonstrateArrayCustomAllocator() {
    std::array<int, 3> arr = {1, 2, 3}; // Create std::array
    std::cout << "std::array elements: ";
    for (const auto& elem : arr) {
        std::cout << elem << " "; // Output elements
    }
    std::cout << std::endl;
}

// 88. std::unique_ptr with custom deleter
void demonstrateUniquePtrCustomDeleter() {
    auto customDeleter = [](int* ptr) {
        std::cout << "Deleting pointer: " << ptr << std::endl;
        delete ptr; // Make sure to delete the pointer
    };

    // Correct way to create unique_ptr with a custom deleter
    std::unique_ptr<int, decltype(customDeleter)> ptr(new int(42), customDeleter);
}

// 89. std::for_each with vector and lambda
void demonstrateForEachLambda() {
    std::vector<int> vec = {1, 2, 3}; // Create vector
    std::for_each(vec.begin(), vec.end(), [](int n) { std::cout << n << " "; }); // Use for_each with lambda
    std::cout << std::endl;
}

// 90. std::accumulate with lambda
void demonstrateAccumulateLambda() {
    std::vector<int> vec = {1, 2, 3}; // Create vector
    int sum = std::accumulate(vec.begin(), vec.end(), 0, [](int a, int b) { return a + b; }); // Calculate sum with lambda
    std::cout << "Sum: " << sum << std::endl; // Output sum
}

// 91. std::transform with lambda
void demonstrateTransformLambda() {
    std::vector<int> vec = {1, 2, 3}; // Create vector
    std::vector<int> squares(vec.size()); // Create vector for squares
    std::transform(vec.begin(), vec.end(), squares.begin(), [](int n) { return n * n; }); // Transform vector with lambda
    std::cout << "Squares: ";
    for (int n : squares) {
        std::cout << n << " "; // Output squares
    }
    std::cout << std::endl;
}

// 92. std::find_if with lambda
void demonstrateFindIfLambda() {
    std::vector<int> vec = {1, 2, 3}; // Create vector
    auto it = std::find_if(vec.begin(), vec.end(), [](int n) { return n > 2; }); // Find element greater than 2
    if (it != vec.end()) {
        std::cout << "Found: " << *it << std::endl; // Output found element
    }
}

// 93. std::remove_if with lambda
void demonstrateRemoveIfLambda() {
    std::vector<int> vec = {1, 2, 3, 4}; // Create vector
    vec.erase(std::remove_if(vec.begin(), vec.end(), [](int n) { return n % 2 == 0; }), vec.end()); // Remove even numbers with lambda
    std::cout << "After remove_if: ";
    for (int n : vec) {
        std::cout << n << " "; // Output modified vector
    }
    std::cout << std::endl;
}

// 94. std::shuffle with lambda
void demonstrateShuffleLambda() {
    std::vector<int> vec = {1, 2, 3, 4, 5}; // Create vector
    std::shuffle(vec.begin(), vec.end(), std::mt19937{std::random_device{}()}); // Shuffle vector with lambda
    std::cout << "Shuffled vector: ";
    for (int n : vec) {
        std::cout << n << " "; // Output shuffled vector
    }
    std::cout << std::endl;
}

// 95. std::variant with lambda visitor
void demonstrateVariantLambdaVisitor() {
    std::variant<int, double> var = 3.14; // Create variant
    std::visit([](auto&& arg) { std::cout << "Variant holds: " << arg << std::endl; }, var); // Visit variant with lambda visitor
}

// 96. std::condition_variable with mutex and lambda
void demonstrateConditionVariableMutexLambda() {
    std::mutex mtx; // Create mutex
    std::condition_variable cv; // Create condition variable
    bool ready = false; // Condition variable state

    std::thread worker([&]() {
        std::unique_lock<std::mutex> lock(mtx); // Lock mutex
        cv.wait(lock, [&ready] { return ready; }); // Wait for condition
        std::cout << "Worker finished!" << std::endl; // Output message
    });

    std::this_thread::sleep_for(std::chrono::seconds(1)); // Simulate work
    {
        std::lock_guard<std::mutex> lock(mtx); // Lock mutex
        ready = true; // Update condition variable state
    }
    cv.notify_one(); // Notify worker
    worker.join(); // Wait for worker to finish
}

// 97. std::shared_ptr with custom deleter lambda
void demonstrateSharedPtrCustomDeleterLambda2() {
    auto sptr = std::shared_ptr<int>(new int(42), [](int* p) {
        std::cout << "Custom deleter lambda called for shared_ptr!" << std::endl; // Custom deleter
        delete p; // Free memory
    });
    std::cout << "Shared Pointer Value: " << *sptr << std::endl; // Output value
}


// 99. std::optional with custom type
struct CustomType {
    int value; // Custom type member
};

void demonstrateOptionalCustomType() {
    std::optional<CustomType> opt; // Create optional for custom type
    std::cout << "Optional value: " << (opt.has_value() ? std::to_string(opt->value) : "none") << std::endl; // Output default value
    opt = CustomType{10}; // Assign value
    std::cout << "Optional value: " << (opt.has_value() ? std::to_string(opt->value) : "none") << std::endl; // Output value
}

// 100. std::array with size deduction
void demonstrateArraySizeDeduction() {
    auto arr = std::array{1, 2, 3}; // Create std::array with size deduction
    std::cout << "std::array elements: ";
    for (const auto& elem : arr) {
        std::cout << elem << " "; // Output elements
    }
    std::cout << std::endl;
}

void demonstrateSFINAE() {
    // Your implementation here
    std::cout << "SFINAE demonstration!" << std::endl;
}

void demonstrateConcepts() {
    // Your implementation here
    std::cout << "Concepts demonstration!" << std::endl;
}


int main() {
    demonstrateSFINAE(); // Call function
    demonstrateConcepts(); // Call function
    demonstrateTemplateSpecialization(); // Call function
    demonstrateStaticVariable(); // Call function
    demonstrateDynamicMemory(); // Call function
    demonstrateFunctionPointer(); // Call function
    demonstrateArrayOfPointers(); // Call function
    demonstrateStructs(); // Call function
    demonstrateUnion(); // Call function
    demonstrateCopy(); // Call function
    demonstrateForEach(); // Call function
    demonstrateFind(); // Call function
    demonstrateSort(); // Call function
    demonstrateReverse(); // Call function
    demonstrateAccumulate(); // Call function
    demonstrateTransform(); // Call function
    demonstrateFindIf(); // Call function
    demonstrateRemoveIf(); // Call function
    demonstrateShuffle(); // Call function
    demonstrateAccumulateCustom(); // Call function
    demonstrateMapLambda(); // Call function
    demonstrateSetCustomComparator(); // Call function
    demonstrateConditionVariableMutex(); // Call function
    demonstrateSharedPtrCustomDeleter(); // Call function
    demonstrateWeakPtr(); // Call function
    demonstrateArray(); // Call function
    demonstrateForward(10); // Call function
    demonstrateMove(); // Call function
    demonstrateVectorCustomAllocator(); // Call function
    demonstrateMoveVector(); // Call function
    demonstrateInitializerList(); // Call function
    demonstrateVariantVisitor(); // Call function
    demonstrateOptionalValueOr(); // Call function
    demonstrateMakeUniqueAndMakeShared(); // Call function
    demonstrateAlignedStorage(); // Call function
    demonstrateVariantLambda(); // Call function
    demonstrateConditionVariableLambda(); // Call function
    demonstrateSharedPtrCustomDeleterLambda(); // Call function
    demonstrateWeakPtrCustomDeleter(); // Call function
    demonstrateArrayCustomAllocator(); // Call function
    demonstrateUniquePtrCustomDeleter(); // Call function
    demonstrateForEachLambda(); // Call function
    demonstrateAccumulateLambda(); // Call function
    demonstrateTransformLambda(); // Call function
    demonstrateFindIfLambda(); // Call function
    demonstrateRemoveIfLambda(); // Call function
    demonstrateShuffleLambda(); // Call function
    demonstrateVariantLambdaVisitor(); // Call function
    demonstrateConditionVariableMutexLambda(); // Call function
    demonstrateOptionalCustomType(); // Call function
    demonstrateArraySizeDeduction(); // Call function
    return 0; // Return statement
}
