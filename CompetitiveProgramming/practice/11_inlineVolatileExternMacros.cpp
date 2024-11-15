#include <iostream>
using namespace std;

#define PI 3.14159 // Macro definition for PI
#define SQUARE(x) ((x) * (x)) // Macro to calculate square of a number

// Extern variable
extern int global_counter;

// Inline function to calculate the area of circle
inline double calculateArea(double radius)
{
    return PI * SQUARE(radius); // using Macros
}

// Volatile
volatile int volatile_counter = 0; // indicates that this var may change any time

// Fn. to simulate an operation that modifies volatile var
void incrementVolatileCounter()
{
    for(int i = 0; i < 5; ++i)
        volatile_counter++; // incrementing volatile var
}

int global_counter = 0; // Definition of extern var

int main() {
    double radius;

    // using inline fn.
    cout << "Enter the circle radius : ";
    cin >> radius;
    cout << "Area => " << calculateArea(radius) << endl;
    
    // using extern
    global_counter = 10;// modifying extern var
    cout << "Global counter => " << global_counter << endl;

    // using volatile var
    incrementVolatileCounter();
    cout << "Volatile Counter => " << volatile_counter << endl;   
}
