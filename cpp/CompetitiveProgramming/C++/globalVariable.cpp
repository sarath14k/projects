#include <iostream>
using namespace std;
int a = 10;

int main()
{

    int a = 1;
    cout << a << endl;   // 1 accessing local variable
    cout << ::a << endl; // 10 accessing global variable
    return 0;
}