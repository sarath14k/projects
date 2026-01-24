#include <iostream>
using namespace std;
// Base class
class Animal {
public:
    virtual void makeSound()  { // Virtual function
        cout << "Some generic animal sound" << endl;
    }

    virtual void eat()  = 0; // Pure virtual function
    virtual ~Animal(){
    }
};

// Derived class: Dog
class Dog : public Animal {
public:
    void makeSound()  { // Override the virtual function
        cout << "Woof!" << endl;
    }

    void eat()  { // Implement the pure virtual function
        cout << "Dog is eating." << endl;
    }
};

// Derived class: Cat
class Cat : public Animal {
public:
    void makeSound() override { // Override the virtual function
        cout << "Meow!" << endl;
    }

    void eat()  override { // Implement the pure virtual function
        cout << "Cat is eating." << endl;
    }
};

int main() {
    Animal* myDog = new Dog();
    Animal* myCat = new Cat();

    myDog->makeSound(); // Outputs: Woof!
    myCat->makeSound(); // Outputs: Meow!

    myDog->eat(); // Outputs: Dog is eating.
    myCat->eat(); // Outputs: Cat is eating.

    delete myDog;
    delete myCat;

    return 0;
}
