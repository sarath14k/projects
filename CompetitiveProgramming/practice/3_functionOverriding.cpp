#include <iostream>
using namespace std;

class Animal
{
    public:
        virtual void sound()
        {
            cout << "Animal makes sound" << '\n';
        }
};
class Dog : public Animal
{
    public:
        void sound()
        {
            cout << "Bow Bow" << '\n';
        }
};

class Cat : public Animal
{
    public:
        void sound()
        {
            cout << "Meow Meow" << '\n';
        }
};

int main() {
    Animal* dog = new Dog();
    Animal* cat = new Cat();

    dog -> sound();
    cat -> sound();

    delete dog;
    delete cat;


}
