#include <iostream>

template <typename T>
T add(T a, T b) {
    return a + b;
}

int main() {
    int sum_int = add(5, 10);
    std::cout << "Sum of integers: " << sum_int << std::endl;

    double sum_double = add(3.5, 2.7);
    std::cout << "Sum of doubles: " << sum_double << std::endl;

    return 0;
}
-----------------------------------------------------------

#include <iostream>
using namespace std;

template <typename T>
class Box
{
private:
    T value;

public:

    Box(T val) : value(val) {}

    T getValue()
    {
        return value;
    }

    void setValue(T val)
    {
        value = val;
    }
};

int main()
{
    // Box of type int
    Box<int> intBox(10);
    cout << "Integer value in Box: " << intBox.getValue() << endl;

    // Box of type float
    Box<float> floatBox(15.5);
    cout << "Float value in Box: " << floatBox.getValue() << endl;

    // Box of type string
    Box<string> stringBox("Hello, Templates!");
    cout << "String value in Box: " << stringBox.getValue() << endl;

    // Set a new value
    stringBox.setValue("C++ is powerful!");
    cout << "Updated string value in Box: " << stringBox.getValue() << endl;

    return 0;
}
----------------------------------------------------------------------------------

#include <iostream>
using namespace std;

// Template class definition
template <typename T>
class Calculator
{
public:
    T num1, num2;

    // Constructor to initialize numbers
    Calculator(T a, T b) : num1(a), num2(b) {}

    // Function to add two numbers
    T add()
    {
        return num1 + num2;
    }

    // Function to subtract two numbers
    T subtract()
    {
        return num1 - num2;
    }

    // Function to multiply two numbers
    T multiply()
    {
        return num1 * num2;
    }

    // Function to divide two numbers
    T divide()
    {
        if (num2 != 0)
            return num1 / num2;
        else
        {
            cout << "Division by zero is not allowed!" << endl;
            return 0;
        }
    }
};

int main()
{
    // Calculator for integers
    Calculator<int> intCalc(10, 5);
    cout << "Integer Addition: " << intCalc.add() << endl;
    cout << "Integer Subtraction: " << intCalc.subtract() << endl;
    cout << "Integer Multiplication: " << intCalc.multiply() << endl;
    cout << "Integer Division: " << intCalc.divide() << endl;

    // Calculator for floating-point numbers
    Calculator<float> floatCalc(5.5, 2.2);
    cout << "\nFloat Addition: " << floatCalc.add() << endl;
    cout << "Float Subtraction: " << floatCalc.subtract() << endl;
    cout << "Float Multiplication: " << floatCalc.multiply() << endl;
    cout << "Float Division: " << floatCalc.divide() << endl;

    return 0;
}
