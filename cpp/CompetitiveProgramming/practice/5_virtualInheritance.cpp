#include <iostream>
using namespace std;

// common base
class Animal
{
    public:
        Animal()
        {
            cout << "Animal Constructor called\n";
        }
        void speak()
        {
            cout << "Animal Speaks\n";
        }
};

//Base 1
class Mammal : virtual public Animal
{
    public:
        Mammal()
        {
            cout << "Mammal Constructor\n";
        }

};
//Base 2
class Bird : virtual public Animal
{
    public:
        Bird()
        {
            cout << "Bird Constructor\n";
        }

};

//Derived 
class Bat : public Mammal, public Bird
{
    public:
        Bat()
        {
            cout << "Bat Constructor\n";
        }
};

int main(){
    Bat myBat;
    myBat.speak();
    return 0;
}
