/*

1. Move Constructor // ClassName(ClassName&& other)  -> MyClass obj3 = std::move(obj1);  

Purpose: The move constructor is used to create a new object by "stealing" the resources from a
temporary (rvalue) or already existing object.

When it's called: The move constructor is invoked when an object is initialized using a temporary
object or an rvalue reference.

2. Move Assignment Operator // ClassName& operator=(ClassName&& other) -> obj2 = std::move(obj3);

Purpose: The move assignment operator is used to "steal" resources from an existing object and assign
them to an already initialized object.
When it's called: The move assignment operator is invoked when an already existing object is assigned
the value of another temporary object or rvalue refer

*/

#include <iostream>

class MyClass
{
public:
    int *data;

    // Constructor
    MyClass(int value)
    {
        data = new int(value);
        std::cout << "Constructor: allocating resource\n";
    }

    // Destructor
    ~MyClass()
    {
        delete data;
        std::cout << "Destructor: freeing resource\n";
    }

    // Move Constructor
    MyClass(MyClass &&other) noexcept
    {
        data = other.data;    // Steal the resource
        other.data = nullptr; // Leave 'other' in a safe state
        std::cout << "Move Constructor: transferring resource\n";
    }

    // Move Assignment Operator
    MyClass &operator=(MyClass &&other) noexcept
    {
        if (this != &other)
        {
            delete data;          // Free existing resource
            data = other.data;    // Steal the resource
            other.data = nullptr; // Leave 'other' in a safe state
            std::cout << "Move Assignment: transferring resource\n";
        }
        return *this;
    }

    // Display the value of the resource
    void print() const
    {
        if (data)
        {
            std::cout << "Value: " << *data << "\n";
        }
        else
        {
            std::cout << "No resource\n";
        }
    }
};

int main()
{
    MyClass obj1(10); // Constructor
    MyClass obj2(20); // Constructor

    // Move Constructor (when creating a new object from a temporary or rvalue)
    MyClass obj3 = std::move(obj1); // Move constructor called
    obj3.print();
    obj1.print(); // obj1 is now in an empty state (nullptr)

    // Move Assignment (assigning to an already existing object)
    obj2 = std::move(obj3); // Move assignment called
    obj2.print();
    obj3.print(); // obj3 is now in an empty state (nullptr)

    return 0;
}
