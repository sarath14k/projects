#include <iostream>
#include <string>
using namespace std;

string removeChar(string &str, char key) {
    int j = 0;
    for (int i = 0; str[i] != '\0'; i++) {
        if (str[i] != key) {
            str[j++] = str[i]; // Copy characters other than key to the front of the string
        }
    }
    str.resize(j); // Resize the string to remove the extra characters
    return str;
}

int main() {
    string res = removeChar("Shameem", 'm');
    cout << res << endl; // Output: Shaee
    return 0;
}
