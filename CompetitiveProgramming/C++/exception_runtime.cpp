#include <iostream>
#include <stdexcept> // Include for std::runtime_error
using namespace std;

int main() {
    try {
        int numerator = 10;
        int denominator = 0;

        if (denominator == 0) {
            throw runtime_error("Denominator can't be zero for division");
        }

        int result = numerator / denominator;
        cout << "Result: " << result << endl;

        throw 10; // Throwing an integer
    }
    catch (int e) // Catching an integer
    {
        cout << "Exception caught: " << e << endl;
    }
    catch (const runtime_error &e) // Catch runtime exception
    {
        cout << "Exception caught: " << e.what() << endl;
    }
    catch (...) // Catch-all for any type of exception
    {   
        cout << "Caught an exception of unknown type!" << endl;
    }

    return 0;
}

/*
When does runtime_error actually happen?
----------------------------------------

The runtime_error exception is thrown when a function or operation fails due to a runtime condition, such as
- Division by zero
- Out-of-range values
- Invalid arguments

In real-world scenarios, a runtime_error exception is typically thrown when the program encounters an 
unexpected condition during execution that can't be resolved. These errors usually occur at runtime 
(as the name suggests), as opposed to compile-time errors, and include situations like:

Invalid calculations (e.g., dividing by zero).
Accessing invalid memory.
File handling issues (e.g., trying to open a file that doesn’t exist).
Out-of-range errors (e.g., accessing an invalid index of an array).


*/
