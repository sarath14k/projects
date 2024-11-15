#include <iostream>
using namespace std;

class Counter {
    private :
        mutable int count; // Mutable member variable
    public :
            Counter() : count(0) {} // Initialize count to zero
            void increment() const {
                ++count; // allowed count because it is mutable
            }

            int getCount() const{
                return count;
            }
};

int main()
{
    const Counter counter; //Const object

    // call increment multiple times on const object
    counter.increment();
    counter.increment();
    counter.increment();

    cout << "\nCount : " << counter.getCount() << endl;
    return 0;
}
