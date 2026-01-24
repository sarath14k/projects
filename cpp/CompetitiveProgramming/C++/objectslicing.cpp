#include <iostream>
using namespace std;

class Base
{
public:
    Base()
    {
        cout << "Base constructor" << endl;
    }
    void show()
    {
        cout << "Base show function" << endl;
    }
};

class Derived : public Base
{
public:
    Derived()
    {
        cout << "Derived constructor" << endl;
    }
    void show()
    {
        cout << "Derived show function" << endl;
    }
};

int main()
{
    Base b = Derived(); // Object slicing occurs here
    b.show();           // Will call Base's show function, not Derived's

    return 0;
}

/* OUTPUT

    Base constructor
    Derived constructor
    Base show function

*/
/*

When you directly assign a Derived object to a Base object like this, object slicing happens.
The derived - specific properties and methods(the part of the Derived object) are "sliced off," 
and only the base part is copied into b.So, this method is generally not recommended unless you 
only need the base part of the object.

*/

/*
1. Creating Simpler Copies of Derived Objects : 

If you need a simpler, more generalized version of a 
derived object, object slicing can help create a "reduced" version of the object by converting it into 
a base class object.This can be useful in data transfer or serialization cases where you only need the 
base class information.
*/
class Shape
{
public:
    virtual void draw()
    {
        cout << "Drawing a generic shape" << endl;
    }
};

class Circle : public Shape
{
public:
    void draw() override
    {
        cout << "Drawing a circle" << endl;
    }
};

int main()
{
    Circle circle;
    Shape simpleShape = circle; // Object slicing
    simpleShape.draw();         // Calls Shape's draw function, not Circle's
}

// op : Drawing a generic shape

/*
2. Copying Derived Object Data into Base Object
    Sometimes, you may only need the base class portion of an object and not care about the extra 
    information in the derived class. Object slicing can be a deliberate action when you want to 
    discard derived class-specific attributes and just focus on the base class behavior.
*/
#include <iostream>
using namespace std;

class Employee
{
public:
    string name;
    Employee(string name) : name(name) {}
    virtual void display()
    {
        cout << "Employee: " << name << endl;
    }
};

class Manager : public Employee
{
public:
    int teamSize;
    Manager(string name, int teamSize) : Employee(name), teamSize(teamSize) {}
    void display() override
    {
        cout << "Manager: " << name << ", Team Size: " << teamSize << endl;
    }
};

void printEmployee(Employee emp)
{
    emp.display(); // Employee's version of display() is called, object slicing happens here
}

int main()
{
    Manager mgr("Alice", 5);
    printEmployee(mgr); // Slices off Manager-specific info and uses Employee portion
    return 0;
}
// op: Employee: Alice
// The printEmployee() function takes an Employee object by value. When a Manager object is passed to it, 
// the Manager-specific information (teamSize) is sliced off, leaving only the Employee part.