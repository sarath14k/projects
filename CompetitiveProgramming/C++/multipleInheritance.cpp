#include <iostream>
using namespace std;

class A
{
public:
    A() { cout << "A's constructor called" << endl; }
    ~A() { cout << "A's Destrcutor called" << endl; }
};

class B
{
public:
    B() { cout << "B's constructor called" << endl; }
    ~B() { cout << "B's Destrcutor called" << endl; }
};

class C : public B, public A // Note the order
{
public:
    C() { cout << "C's constructor called" << endl; }
    ~C() { cout << "C's Destrcutor called" << endl; }
};

int main()
{
    C c;
    return 0;
}

// constructors ->  B's constructor called
//                  A's constructor called
//                  C's constructor called

// destructors ->   C's Destrcutor called
//                  A's Destrcutor called
//                  B's Destrcutor called


// Diomond problem 
#include <iostream>
using namespace std;
class Person
{
public:
    Person(int x) { cout << "Person::Person(int ) called" << endl; }
    Person() { cout << "Person::Person() called" << endl; }
};

class Faculty : virtual public Person
{
public:
    Faculty(int x) : Person(x)
    {
        cout << "Faculty::Faculty(int ) called" << endl;
    }
};

class Student : virtual public Person
{
public:
    Student(int x) : Person(x)
    {
        cout << "Student::Student(int ) called" << endl;
    }
};

class TA : public Faculty, public Student
{
public:
    TA(int x) : Student(x), Faculty(x)
    {
        cout << "TA::TA(int ) called" << endl;
    }
};

int main()
{
    TA ta1(30);
}

/*

Person::Person() called
Faculty::Faculty(int ) called
Student::Student(int ) called
TA::TA(int ) called

One important thing to note in the above output is, the default constructor of ‘Person’ is called.
When we use ‘virtual’ keyword, the default constructor of grandparent class is called by default
even if the parent classes explicitly call parameterized constructor.

How to call the parameterized constructor of the ‘Person’ class?
We can call the parameterized constructor of the ‘Person’ class by using the ‘Person’ constructor
explicitly in the ‘TA’ class constructor.
TA::TA(int x) : Person(x), Student(x), Faculty(x)


*/

class TA : public Faculty, public Student  {
public:
    TA(int x):Student(x), Faculty(x), Person(x)   {
        cout<<"TA::TA(int ) called"<< endl;
    }
};

The "diamond problem" in C++ arises when two classes B and C inherit from a common base class A,
    and another class D inherits from both B and C.This creates an ambiguity because D has two copies of A.The issue can be resolved using virtual inheritance.

#include <iostream>

        class A
{
public:
    void show()
    {
        std::cout << "Class A" << std::endl;
    }
};

class B : public A
{
};

class C : public A
{
};

class D : public B, public C
{
};

int main()
{
    D obj;
    // obj.show(); // Error: request for member ‘show’ is ambiguous
    obj.B::show(); // This works, but you need to specify which path to use
    obj.C::show(); // This also works, but again, you need to specify
    return 0;
}

//resolving using virtual inheritance

#include <iostream>

class A
{
public:
    void show()
    {
        std::cout << "Class A" << std::endl;
    }
};

class B : virtual public A
{
};

class C : virtual public A
{
};

class D : public B, public C
{
};

int main()
{
    D obj;
    obj.show(); // Now this works without ambiguity
    return 0;
}

Without Virtual Inheritance :

    Class B and class C both inherit from class A.
    Class D inherits from both B and C,
    resulting in two instances of class A.
    This causes ambiguity when calling a method from class A.
    
With Virtual Inheritance :

class B : virtual public A 
and 
class C : virtual public A 
ensure that only one instance of class A 
is shared between B and C.This resolves the ambiguity and 
allows class D to inherit a single instance of class A.