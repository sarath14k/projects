#include <iostream>
using namespace std;
class Base
{
    int a;

public:
    virtual void pureVirtual() = 0;

    Base(int data) : a(data) {}
    void print()
    {
        cout << "a : " << a << endl;
    }

   
};

class Derived : public Base
{

public:
    Derived(int k) : Base(k) {}

    void pureVirtual() override
    {
        cout << "derived pure" << endl;
    }
};

int main()
{
    Derived d(10);
    d.print();
    return 0;
}



