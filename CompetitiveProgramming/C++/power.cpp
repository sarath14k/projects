#include <iostream>
using namespace std;

int main()
{

    float x, y;
    cout << "enter the number" << endl;
    cin >> x;
    cout << "enter the exponent" << endl;
    cin >> y;
    float res = 1;

    int exponent = y < 0 ? -static_cast<int>(y) : static_cast<int>(y);
    cout << exponent << endl;

    for (int i = 0; i < exponent; i++)
    {
        res = res * x;
    }

    if (y < 0)
    {
        res = 1 / res;
    }

    cout << "x power of y " << res << endl;
    return 0;
}
