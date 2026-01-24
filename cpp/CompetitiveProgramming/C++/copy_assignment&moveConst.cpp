/*

The copy assignment operator in C++ is used to assign one object to another already existing object of the same class. 
It allows you to copy the content of one object to another object.

this example contains deep copy ,shallow copy, copy assignment operator, copy constructor
*/
#include <iostream>
using namespace std;

class Sample
{
private:
    int a;
    string str;

public:
    // Default constructor
    Sample() : a(0), str("") {}

    // Parameterized constructor
    Sample(int data, string strData) : a(data), str(strData) {}

    // Copy constructor
    Sample(const Sample &obj) : a(obj.a), str(obj.str) {}

    // Copy assignment operator
    Sample &operator=(const Sample &obj)
    {
        if (this != &obj)
        { // Check for self-assignment
            a = obj.a;
            str = obj.str;
        }
        return *this;
    }
};

int main()
{
    Sample obj1(10, "Hello"); // Create object with parameterized constructor
    Sample obj2;              // Create object with default constructor

    obj2 = obj1; // Copy assignment operator is called here

    // Output the copied values
    cout << "Value of a: " << obj2.a << endl;
    cout << "Value of str: " << obj2.str << endl;

    return 0;
}


/*********************************************************************************************** */

#include <iostream>
using namespace std;

class MyClass
{
private:
    int *data;
    int size;

public:
    // Default constructor
    MyClass() : data(nullptr), size(0)
    {
        cout << "Default Constructor: no memory allocated\n";
    }

    // Parameterized constructor
    MyClass(int s) : size(s)
    {
        data = new int[size];
        cout << "Constructor: allocated memory\n";
    }

    // Copy constructor
    MyClass(const MyClass &other) : size(other.size)
    {
        // Allocate new memory and perform deep copy
        data = new int[size];
        for (int i = 0; i < size; ++i)
        {
            data[i] = other.data[i];
        }
        cout << "Copy Constructor: copied data\n";
    }

    // Shallow copy constructor (problematic)
    MyClass(const MyClass &other) : size(other.size), data(other.data)
    {
        // No deep copy, just copying the pointer
        cout << "Shallow Copy Constructor: pointer copied, no new allocation\n";
    }

    // Destructor
    ~MyClass()
    {
        delete[] data;
        cout << "Destructor: freed memory\n";
    }

    // Copy assignment operator
    MyClass &operator=(const MyClass &other)
    {
        if (this == &other)
        { // Check for self-assignment
            return *this;
        }

        // Free existing memory
        delete[] data;

        // Allocate new memory and deep copy the data
        size = other.size;
        data = new int[size];
        for (int i = 0; i < size; ++i)
        {
            data[i] = other.data[i];
        }

        // Shallow copy: copy the pointer and size only
        size = other.size;
        data = other.data; // No deep copy , just copying the pointer - problamatic !!!


        cout << "Copy assignment operator: copied data\n";
        return *this; // Return reference to the current object
    }

    // Move constructor
    MyClass(MyClass&& other) noexcept
        : data(other.data), size(other.size) {
        // Steal the data from the other object
        other.data = nullptr;  // Set the source object's data to nullptr
        other.size = 0;        // Reset its size
        cout << "Move Constructor: moved resource\n";
    }

    // Function to print data
    void print() const
    {
        for (int i = 0; i < size; ++i)
        {
            cout << data[i] << " ";
        }
        cout << endl;
    }

    // Function to set data
    void setData(int index, int value)
    {
        if (index >= 0 && index < size)
        {
            data[index] = value;
        }
    }
};

int main()
{
    MyClass obj1();  // default
    MyClass obj2(2); // Create object with size 2 - parameterized 
    obj1.setData(0, 10);
    obj1.setData(1, 20);

    obj1 = obj2 ; // copy assignment operator

    MyClass obj3 = obj1; // Use copy constructor here
    
    MyClass obj4 = std::move(obj2); // Move constructor is called

    obj2.print(); // Print obj2 to see copied data

    return 0;
}
