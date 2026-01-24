
#include <bits/stdc++.h>
using namespace std;

void swap(int a, int b)
{

    a = a + b;
    b = a - b;
    a = a - b;

    cout << "a :" << a << endl;
    cout << "b :" << b << endl;
}

void reverseNum(int a)
{

    cout << "ori int " << a << endl;

    int rev = 0;
    int n;

    while (a > 0)
    {
        n = a % 10;
        rev = rev * 10 + n;
        a = a / 10;
    }

    cout << "rev int " << rev << endl;
}

void reverseString(const string &str)
{

    cout << "ori str " << str << endl;

    int size = str.length();
    for (int i = size - 1; i >= 0; i--)
    {
        cout << str[i];
    }
}

void fibonocii(int limit)
{
    int a = 0;
    int b = 1;
    int c = 0;

    if (limit >= 1)
        cout << a << "\t";

    if (limit >= 2)
    {
        cout << b << "\t";
    }

    for (int i = 2; i < limit; i++)
    {

        c = a + b;
        cout << c << "\t";
        a = b;
        b = c;
    }
}

void palindrome(int num)
{

    int numCopy = num;

    int n;
    int rev = 0;

    while (numCopy > 0)
    {
        n = numCopy % 10;
        rev = rev * 10 + n;
        numCopy = numCopy / 10;
    }

    if (rev == num)
    {
        cout << "palindrome" << endl;
    }
    else
    {
        cout << "not palindrome " << endl;
    }
}

void palindromeString(const string &str)
{

    string copyStr = "";

    int size = str.length();
    for (int i = size - 1; i >= 0; i--)
    {
        copyStr.push_back(str[i]);
    }

    if (str == copyStr)
    {
        cout << "palindrome" << endl;
    }
    else
    {
        cout << "not palindrome " << endl;
    }
}

void primeNumbers(int lower, int upper)
{

    for (int i = lower; i <= upper; i++)
    {

        if (!(lower % i == 0))
        {

            cout << i << endl;
        }
        lower++;
    }
}

int main()
{
    // swap(10,20);
    // reverseNum(1042);
    // reverseString("Hello");
    // fibonocii(7);
    // palindrome(1221);
    // palindromeString("madam");
    primeNumbers(2, 10);

    return 0;
}