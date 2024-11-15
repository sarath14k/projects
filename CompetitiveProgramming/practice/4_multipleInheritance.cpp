#include <iostream>
using namespace std;

class Car
{
    public:
        void drive()
        {
            cout << "Driving car!\n";
        }
};
class Airplane
{
    public:
        void fly()
        {
            cout << "Flying Airplane!\n";
        }
};
class FlyingCar: public Car, public Airplane
{
    public:
        void travel()
        {
           drive(); // Car's drive method call 
           fly(); // Airplane's fly method call 
        }
};

int main(){
    FlyingCar obj;
    obj.travel();
    return 0;
}
