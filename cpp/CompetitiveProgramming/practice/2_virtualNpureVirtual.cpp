#include <iostream>
using namespace std;

// Base class
class Shape {
public:
    virtual void draw() = 0; // Pure virtual function (forces children to implement it)
};

// Derived class 1
class Circle : public Shape {
public:
    void draw() { cout << "Drawing a Circle" << endl; }
};

// Derived class 2
class Square : public Shape {
public:
    void draw() { cout << "Drawing a Square" << endl; }
};

int main() {
    Circle c;
    Square s;

    // Use a Base class reference to point to different objects
    Shape& s1 = c; 
    Shape& s2 = s;

    s1.draw(); // Outputs: Drawing a Circle
    s2.draw(); // Outputs: Drawing a Square

    return 0;
}
