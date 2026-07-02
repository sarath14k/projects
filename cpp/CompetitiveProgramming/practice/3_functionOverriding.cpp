#include <iostream>
using namespace std;

class Animal {
public:
    virtual void sound() { cout << "Generic Sound\n"; }
};

class Dog : public Animal {
public:
    void sound() override { cout << "Bow Bow\n"; }
};

class Cat : public Animal {
public:
    void sound() override { cout << "Meow Meow\n"; }
};

int main() {
    Dog d; 
    Cat c;

    // Pointing a Base reference to the Child objects triggers polymorphism
    Animal& ref1 = d;
    Animal& ref2 = c;

    ref1.sound(); // Outputs: Bow Bow
    ref2.sound(); // Outputs: Meow Meow
}
