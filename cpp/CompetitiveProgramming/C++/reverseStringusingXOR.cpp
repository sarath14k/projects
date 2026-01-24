#include <iostream>
#include <string>
using namespace std;

void reverseString(string &str)
{
    int n = str.length();
    int start = 0;
    int end = n - 1;

    // Reverse the string using XOR swap
    while (start < end)
    {
        // XOR swap
        str[start] ^= str[end];
        str[end] ^= str[start];
        str[start] ^= str[end];

        start++;
        end--;
    }
}

int main()
{
    string str = "Hello, World!";
    reverseString(str);
    cout << "Reversed string: " << str << endl;
    return 0;
}
