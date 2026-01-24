/*

Shallow copy and deep copy concepts usually apply to situations involving pointers or dynamically 
allocated memory (e.g., new, malloc)

1. Shallow Copy

  A shallow copy simply copies the values of an object's member variables to another object.
  For objects that contain pointers, this means both the original and the copied objects will
  point to the same memory location, potentially leading to issues like double deletion or unintended
  changes.

  A shallow copy copies only the values of the member variables as they are.If a member is a pointer,
  a shallow copy will copy only the pointer's value, not the data it points to. This means both the
  original and the copied object will share the same memory, leading to potential issues.

2. Deep Copy
    A deep copy, on the other hand, creates a new copy of the dynamically allocated memory as well.
    This ensures that changes to the copied object do not affect the original, and both objects manage
    their own memory independently.
*/

#include <iostream>
#include <cstring> // for memcpy

class MyClass
{
public:
    int *data;
    int size;

    // Constructor
    MyClass(int s) : size(s)
    {
        data = new int[s];
        for (int i = 0; i < s; ++i)
        {
            data[i] = i + 1; // Initialize with some values
        }
    }

    // Shallow Copy Constructor (Default Copy Constructor)
    MyClass(const MyClass &other) : size(other.size), data(other.data)
    {
        // This is a shallow copy, just copying the pointer
        std::cout << "Shallow Copy Constructor\n";
    }

    // Deep Copy Constructor
    MyClass(const MyClass &other, bool deepCopy) : size(other.size)
    {
        if (deepCopy)
        {
            data = new int[other.size];                        // Allocate new memory
            std::memcpy(data, other.data, size * sizeof(int)); // Copy contents
            std::cout << "Deep Copy Constructor\n";
        }
        else
        {
            data = other.data; // Shallow copy fallback
        }
    }

    // Destructor
    ~MyClass()
    {
        delete[] data; // Free dynamically allocated memory
        std::cout << "Destructor called\n";
    }

    // Display the contents of the array
    void printData() const
    {
        for (int i = 0; i < size; ++i)
        {
            std::cout << data[i] << " ";
        }
        std::cout << "\n";
    }
};

int main()
{
    MyClass obj1(5); // Create object with size 5
    std::cout << "Original Object (obj1): ";
    obj1.printData();

    // Shallow copy (using default copy constructor)
    MyClass obj2 = obj1;
    std::cout << "Shallow Copied Object (obj2): ";
    obj2.printData();

    // Change obj2's data, this will affect obj1 as well due to shallow copy
    obj2.data[0] = 100;
    std::cout << "After modifying obj2:\n";
    std::cout << "obj1 data: ";
    obj1.printData();
    std::cout << "obj2 data: ";
    obj2.printData();

    // Deep copy
    MyClass obj3(obj1, true);
    std::cout << "Deep Copied Object (obj3): ";
    obj3.printData();

    // Change obj3's data, this will NOT affect obj1 because of deep copy
    obj3.data[0] = 200;
    std::cout << "After modifying obj3:\n";
    std::cout << "obj1 data: ";
    obj1.printData();
    std::cout << "obj3 data: ";
    obj3.printData();

    return 0;
}

Aspect	            Shallow Copy	                                    Deep Copy
Memory Allocation	Copies the pointer, so both objects share memory.	Allocates new memory for the copied object.
Modification	    Modifying one object affects the other.	            Modifying one object does not affect the other.
Destructor	        Can lead to double deletion or dangling pointers.	Safely deletes memory for each object independently.
Use Case	        Useful when you want to share resources '           Needed when each object must own its data.
                    (e.g., reference counting).


When to Use Deep vs. Shallow Copy?
Shallow copy can be appropriate when:
You are dealing with small objects that don’t manage external resources like dynamic memory.
You intend to share the data between multiple objects (e.g., reference-counted objects).


Deep copy is required when:
The object manages dynamic resources (like memory, file handles, network connections) that need to be independently managed by each object.
You want to avoid the risk of one object affecting another after a copy.


In Conclusion:
Shallow Copy: Just copies pointers, resulting in multiple objects pointing to the same memory.
Deep Copy: Duplicates the memory itself, making each object independent from others

  */