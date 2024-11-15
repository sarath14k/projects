#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

// Merged Solution class for characterReplacement
class Solution {
public:
    int characterReplacement(string s, int k) {
        vector<int> charCount(26, 0);  // Array to count occurrences of each character
        int maxCharCount = 0;           // Variable to store the count of the most frequent character in the current window

        int left = 0;             // Left pointer for the sliding window
        int right = 0;            // Right pointer for the sliding window

        int maxLength = 0;               // Variable to store the maximum length of substring found

        // Iterate through the string with the right pointer
        while (right < s.size()) {
            // Count the current character
            charCount[s[right] - 'A']++;
            // Update the maximum count of a single character in the current window
            maxCharCount = max(maxCharCount, charCount[s[right] - 'A']);

            // If the number of characters to replace exceeds k
            if (right - left + 1 - maxCharCount > k) {
                // Move the left pointer to reduce the window size
                charCount[s[left] - 'A']--;
                left++;
            }

            // Update the maximum length of valid substring found
            maxLength = max(maxLength, right - left + 1);
            right++;  // Move the right pointer to expand the window
        }

        return maxLength;  // Return the maximum length of substring found
    }
    /*
    Time Complexity: O(n), where n is the length of the string s.
    Space Complexity: O(1), since the size of the charCount array is constant (26).
    */
};

// Main function to test the solution
int main() {
    Solution solution;

    // Test case
    string s = "AABABBA";
    int k = 1;

    // Test the characterReplacement method
    int result = solution.characterReplacement(s, k);
    cout << "Length of the longest substring after replacement: " << result << endl;

    return 0;
}
