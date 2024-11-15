#include <iostream>
#include <string>
using namespace std;

// Original Solution class to check if a string is a palindrome
class Solution {
public:
    bool isPalindrome(string s) {
        int l = 0, r = s.length() - 1;

        while (l < r) {
            // Move left pointer to the next alphanumeric character
            while (l < r && !isalnum(s[l])) l++;

            // Move right pointer to the previous alphanumeric character
            while (l < r && !isalnum(s[r])) r--;

            // Compare characters ignoring case
            if (tolower(s[l]) != tolower(s[r])) return false;

            // Move both pointers towards the center
            l++;
            r--;
        }
        return true;
    }
};

    // Function to check if a character is alphanumeric
    bool isAlphanumeric(char c) {
        return (c >= 'A' && c <= 'Z' ||
                c >= 'a' && c <= 'z' ||
                c >= '0' && c <= '9');
    }
    /*
    Time Complexity: O(n), where n is the length of the input string, as we scan through the string.
    Space Complexity: O(1), since we only use a few extra variables.
    */

// Simple main function to test both versions
int main() {

    Solution optimizedSol;
    // Test case: Example input
    string testString = "A man, a plan, a canal: Panama";
    // Test the optimized solution
    bool optimizedResult = optimizedSol.isPalindrome(testString);
    cout << "Optimized Solution Result: " << (optimizedResult ? "Palindrome" : "Not a palindrome") << endl;
    return 0;
}
