#include <iostream>
#include <string>
using namespace std;

// Original Solution class to check if a string is a palindrome
class OriginalSolution {
public:
    // Function to determine if the string is a palindrome (original version)
    bool isPalindrome(string s) {
        int leftIndex = 0; // Left pointer
        int rightIndex = s.length() - 1; // Right pointer

        // Loop until the pointers meet
        while (leftIndex < rightIndex) {
            // Move left pointer to the right while it's not alphanumeric
            while (leftIndex < rightIndex && !isAlphanumeric(s[leftIndex])) {
                leftIndex++;
            }
            // Move right pointer to the left while it's not alphanumeric
            while (rightIndex > leftIndex && !isAlphanumeric(s[rightIndex])) {
                rightIndex--;
            }
            // Check if the characters at both pointers are the same (case-insensitive)
            if (tolower(s[leftIndex]) != tolower(s[rightIndex])) {
                return false; // Not a palindrome
            }
            leftIndex++; // Move left pointer
            rightIndex--; // Move right pointer
        }
        return true; // It's a palindrome
    }

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
};

// Optimized Solution class to check if a string is a palindrome
class Solution {
public:
    // Function to determine if the string is a palindrome (optimized version)
    bool isPalindrome(string s) {
        int leftIndex = 0; // Left pointer
        int rightIndex = s.length() - 1; // Right pointer

        // Loop until the pointers meet
        while (leftIndex < rightIndex) {
            // Move left pointer to the right while it's not alphanumeric
            while (leftIndex < rightIndex && !isAlphanumeric(s[leftIndex])) {
                leftIndex++;
            }
            // Move right pointer to the left while it's not alphanumeric
            while (rightIndex > leftIndex && !isAlphanumeric(s[rightIndex])) {
                rightIndex--;
            }
            // Check if the characters at both pointers are the same (case-insensitive)
            if (tolower(s[leftIndex]) != tolower(s[rightIndex])) {
                return false; // Not a palindrome
            }
            leftIndex++; // Move left pointer
            rightIndex--; // Move right pointer
        }
        return true; // It's a palindrome
    }

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
};

// Simple main function to test both versions
int main() {
    OriginalSolution originalSol;
    Solution optimizedSol;

    // Test case: Example input
    string testString = "A man, a plan, a canal: Panama";

    // Test the original solution
    bool originalResult = originalSol.isPalindrome(testString);
    cout << "Original Solution Result: " << (originalResult ? "Palindrome" : "Not a palindrome") << endl;

    // Test the optimized solution
    bool optimizedResult = optimizedSol.isPalindrome(testString);
    cout << "Optimized Solution Result: " << (optimizedResult ? "Palindrome" : "Not a palindrome") << endl;

    return 0;
}
