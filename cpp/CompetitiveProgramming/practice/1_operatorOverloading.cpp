#include <iostream>
using namespace std;

class Complex{
    double real, imag;
    public:
        Complex(double r, double i) : real(r), imag(i) {}

        //Overloading '+' operator
        Complex operator+(const Complex& other)
        {
            return Complex(real + other.real, imag + other.imag);
        }

        void display()
        {
            cout << this->real << '+' << this->imag << 'i'<< endl;
        }

};

int main()
{
    Complex c1(1.0,2.0);
    Complex c2(2.0,3.0);

    // Uses overloaded '+' operator
    Complex c3 = c1 + c2;
    c3.display();

    return 0;
}
