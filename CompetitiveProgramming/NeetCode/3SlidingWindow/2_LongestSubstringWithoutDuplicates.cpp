#include <iostream>
#include <unordered_set>
#include <string>
#include <algorithm>

using namespace std;

// Merged Solution class for lengthOfLongestSubstring
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        unordered_set<char> uniqueChars;  // Set to store unique characters in the current window
        int leftPointer = 0;               // Left pointer for the sliding window
        int maxLength = 0;                 // Variable to store the maximum length found

        // Iterate through the string with the right pointer
        for (int rightPointer = 0; rightPointer < s.size(); rightPointer++) {
            // While the character at the right pointer is already in the set
            while (uniqueChars.find(s[rightPointer]) != uniqueChars.end()) {
                uniqueChars.erase(s[leftPointer]);  // Remove the leftmost character
                leftPointer++;                       // Move the left pointer to the right
            }
            uniqueChars.insert(s[rightPointer]);  // Add the current character to the set
            maxLength = max(maxLength, rightPointer - leftPointer + 1);  // Update maxLength
        }
        return maxLength;  // Return the maximum length of substring found
    }
    /*
    Time Complexity: O(n), where n is the length of the string s.
    Space Complexity: O(min(n, m)), where m is the size of the character set.
    */
};

// Main function to test the solution
int main() {
    Solution solution;

    // Test case
    string s = "abcabcbb";

    // Test the lengthOfLongestSubstring method
    int result = solution.lengthOfLongestSubstring(s);
    cout << "Length of the longest substring without repeating characters: " << result << endl;

    return 0;
}
