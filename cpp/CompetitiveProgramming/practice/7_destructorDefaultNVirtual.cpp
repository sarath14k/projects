#include <iostream>
using namespace std;
class Base
{
    public:
        Base() { cout << "Base constructor\n"; }
        virtual ~Base() { cout << "Base destructor\n"; }
};


class Derived : public Base 
{
    public:
        Derived() { cout << "Derived constructor\n"; }
        ~Derived() { cout << "Derived destructor\n"; }
};

int main() {
    Base *obj =  new Derived(); // Upcast to base ptr
    delete obj; // Only calls if Base destr if not virtual
    return 0;
}
