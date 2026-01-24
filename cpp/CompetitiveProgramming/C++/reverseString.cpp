#include <iostream>
#include <string>
using namespace std;

void reverseString(string &str)
{
    int n = str.length();
    // Convert string to character array (it's already done internally by string in C++)
    char charArray[n + 1];
    strcpy(charArray, str.c_str());

    // Use two pointers to reverse the string
    int start = 0;
    int end = n - 1;
    while (start < end)
    {
        // Swap characters
        swap(charArray[start], charArray[end]);
        start++;
        end--;
    }

    // Assign the reversed character array back to the string
    str = string(charArray);
}

int main()
{
    string str = "Hello, World!";
    reverseString(str);
    cout << "Reversed string: " << str << endl;
    return 0;
}
