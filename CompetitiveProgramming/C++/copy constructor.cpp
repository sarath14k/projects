#include <iostream>

class MyClass
{
public:
    int data;

    // Default constructor
    MyClass() : data(0) {}

    // Parameterized constructor
    MyClass(int value) : data(value) {}

    // Copy constructor
    MyClass(const MyClass &other) : data(other.data) {}

    // Member function to display data
    void display()
    {
        std::cout << "Data: " << data << std::endl;
    }
};

int main()
{
    // Creating objects
    MyClass obj1(10);
    MyClass obj2(obj1); // Using the copy constructor

    // Displaying data
    obj1.display(); // Output: Data: 10
    obj2.display(); // Output: Data: 10

    return 0;
}

/* A copy constructor in C++ is a special type of constructor that is used to create a new object
as a copy of an existing object.It takes an object of the same class as its parameter and creates
a new object with the same data members as the original object.

In this example, MyClass has a copy constructor MyClass(const MyClass& other) which takes a 
reference to another object of type MyClass. When obj2 is created using obj1, 
the copy constructor is invoked, and obj2 is initialized with the same data as obj1.

*/

/*

#include <iostream>
using namespace std;
class Base
{
private:
    int d;

public:
    Base(int data) : d(data) {}
    Base(Base &obj) : d(obj.d) {} // copy constructor
    friend void demoFriend(Base b);
};
void demoFriend(Base b)
{
    cout << b.d << endl;
}
int main()
{
    Base b(50);
    Base b1 = b;
    demoFriend(b1);
    return 0;
}

*/