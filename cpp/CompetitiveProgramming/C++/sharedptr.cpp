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

    Foo *ptr = new Foo(10);
    delete ptr;
    
    std::shared_ptr<Foo> sp(new Foo(10));
    cout<<sp->getX()<<endl;
    cout<<sp.use_count()<<endl;
    
    std::shared_ptr<Foo> sp1 = sp;
    cout<<sp1.use_count()<<endl;
    return 0;
}


shared_ptr<Foo> sp = make_shared<Foo>(10);
shared_ptr<Foo>sp(new Foo(10));

unique_ptr<Foo> up(new Foo(10));
unique_ptr<Foo> up1 =make_unique<Foo>(10);
