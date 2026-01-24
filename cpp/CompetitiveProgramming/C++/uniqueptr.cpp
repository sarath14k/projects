/*  Unique pointers in C++ are smart pointers that provide exclusive ownership semantics. 
This means that a unique pointer can point to an object, and only one unique pointer can own 
that object at a time
*/
#include <iostream>
#include <memory>
using namespace std;

class Foo{
    private:
        int x;
    public:
        Foo(int x):x(x){}
        int getX(){
            return x;
        }
    ~Foo(){
        cout <<"Destructor" << endl;
    }
};

int main() {
    
    // normal pointer
    Foo *f = new Foo(20);
    cout << f->getX() << endl;
    delete f;
    
    //unique pointer - no need to delete
    unique_ptr<Foo> p(new Foo(10));
    cout << p->getX() << endl;
    
    unique_ptr<Foo> p1 = make_unique<Foo>(20);
    cout << (*p1).getX() << endl;
    
    // p1 = p; // FAIL 
    
    unique_ptr<Foo> p2 = std::move(p1);
    cout <<"p2  "<< (*p2).getX() << endl;
    
    Foo * p4 = p.release();
    p2.reset(p4);
    cout <<"p2  "<< (*p2).getX() << endl;


    return 0;
}