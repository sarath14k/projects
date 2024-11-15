#include <iostream>
using namespace std;

struct student
{
    char a;
    char b;
    int c;
};

int main()
{
    std::cout << sizeof(student) << endl;
    return 0;
}

Theoretically, the total size should be 1(a) + 1(b) + 4(c) = 6 bytes.However, due to memory alignment, 
the compiler typically adds padding to ensure that members of a structure are properly aligned in memory.
On most systems,the int field(4 bytes) is aligned to a 4 - byte boundary.Therefore, after the two char 
fields(2 bytes total), the compiler will add 2 bytes of padding before the int field.
This results in a total size of 8 bytes.

If you run this program,
you'll likely see that sizeof(student) returns 8 due to this padding.
To visualize :

    a(1 byte) | b(1 byte) | padding(2 bytes) | c(4 bytes) |
    Total : 8 bytes.