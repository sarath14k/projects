#include <iostream>
#include <string>
#include <std
using namespace std;

int main()
{
    int denominator = 0;
    int numerator = 5;

    try {
        if (denominator == 0) {
            throw "Denominator can't be zero for division";
        }
        int res = numerator / denominator;
        cout << "res : " << res << endl;

    } catch (const char* msg) {
        cout << "Exception: " << msg << endl;
    }

    return 0;
}
