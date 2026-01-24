/*
A pointer constant(also known as a constant pointer) in C++ is a pointer whose address it holds is constant, 
meaning once it is initialized to point to a specific memory location, you cannot change the address it points to.
However, you can still modify the value of the data at the memory location the pointer is pointing to.

int* const ptr;

means ptr is a constant pointer to an integer.The address stored in ptr cannot be changed after initialization,
    but you can still modify the value at the address.

    1. The pointer itself is constant,
    2. not the value it points to.The value the pointer points to can be modified.
    3.You must initialize a constant pointer when declaring it because it can't be assigned a new address later

*/

#include <iostream>
using namespace std;

int main()
{
    int a = 10;
    int b = 20;

    int *const ptr = &a; // Constant pointer to int, must be initialized

    *ptr = 15; // Modifying the value at the location 'ptr' is pointing to (allowed)

    // ptr = &b;  // Error! Cannot change the address stored in a constant pointer

    cout << "Value at ptr: " << *ptr << endl; // Outputs: 15

    return 0;
}

 /*
Difference Between Constant Pointer and Pointer to Constant : 

Constant Pointer(int *const) : The pointer itself is constant, but the value it points to can be changed.
Pointer to Constant(const int *) : The pointer can point to different addresses, but the value at the address 
                                   the pointer is pointing to cannot be modified through the pointer.
*/

const int *p1; // Pointer to a constant int (you can't modify the value pointed to)
int* const p2; // Constant pointer to an int (you can't change the pointer itself)

#include <iostream>
using namespace std;

int main()
{
    int a = 10;
    int b = 20;

    const int *ptr = &a; // Pointer to a constant int

    // *ptr = 15;  // Error! Cannot modify the value through a pointer to constant

    ptr = &b; // Changing the pointer to point to another address is allowed

    cout << "Value at ptr: " << *ptr << endl; // Outputs: 20

    return 0;
}
