#include <iostream>
#include <string>
using namespace std;

bool compareStringsUsingXOR(const string &str1, const string &str2)
{
    // If lengths are different, strings are not equal
    if (str1.length() != str2.length())
    {
        return false;
    }

    // XOR all characters of the strings
    char result = 0;
    for (size_t i = 0; i < str1.length(); ++i)
    {
        result ^= (str1[i] ^ str2[i]);
    }

    // If result is 0, strings are equal; otherwise, they are not
    return result == 0;
}

int main()
{
    string str1 = "hello";
    string str2 = "hello";
    string str3 = "world";

    if (compareStringsUsingXOR(str1, str2))
    {
        cout << "str1 and str2 are equal" << endl;
    }
    else
    {
        cout << "str1 and str2 are not equal" << endl;
    }

    if (compareStringsUsingXOR(str1, str3))
    {
        cout << "str1 and str3 are equal" << endl;
    }
    else
    {
        cout << "str1 and str3 are not equal" << endl;
    }

    return 0;
}
