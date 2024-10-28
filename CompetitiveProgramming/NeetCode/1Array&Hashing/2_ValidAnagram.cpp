#include <iostream>
#include <unordered_map>
#include <string>
using namespace std;

// Original Solution class to check if two strings are anagrams
class OriginalSolution {
public:
    // Function to determine if string s is an anagram of string t
    bool isAnagram(string s, string t) {
        // If the sizes of the strings are not the same, they cannot be anagrams
        if (s.size() != t.size())
            return false;

        // Unordered map to keep a count of each character in the strings
        unordered_map<char, int> charCount;

        // Count each character from string 's'
        for (char c : s)
            charCount[c]++;

        // Decrease the count of each character from string 't'
        for (char c : t) {
            // If a character is not found in 's' or count reaches zero, it's not an anagram
            if (charCount[c] == 0)
                return false;
            charCount[c]--;
        }

        // Check if all character counts are zero, indicating all characters matched
        for (auto count : charCount)
            if (count.second != 0)
                return false;

        // If everything matched, return true
        return true;
    }
    /*
    Time Complexity: O(n) where n is the length of the strings, as we need to iterate through both strings.
    Space Complexity: O(1) since the unordered map can have at most 26 characters (if only lowercase letters are considered).
    */
};

// Optimized Solution class to check if two strings are anagrams
class Solution {
public:
    // Optimized function to determine if string s is an anagram of string t
    bool isAnagram(string s, string t) {
        // If the sizes of the strings are not the same, they cannot be anagrams
        if (s.size() != t.size())
            return false;

        // Unordered map to keep a count of each character in the strings
        unordered_map<char, int> charCount;

        // Count each character from string 's'
        for (char c : s)
            charCount[c]++;

        // Decrease the count of each character from string 't'
        for (char c : t) {
            // If a character is not found in 's' or count reaches zero, it's not an anagram
            if (charCount[c]-- == 0) // Decrement and check in one step
                return false;
        }

        // If everything matched, return true
        return true;
    }
    /*
    Time Complexity: O(n) where n is the length of the strings, as we need to iterate through both strings.
    Space Complexity: O(1) since the unordered map can have at most 26 characters (if only lowercase letters are considered).
    */
};

// Simple main function to test both versions
int main() {
    // Create instances of both Original and Optimized Solution classes
    OriginalSolution originalSol;
    Solution optimizedSol;  // Using just "Solution" for the optimized version

    // Test case 1: Anagram
    string s1 = "anagram";
    string t1 = "nagaram";
    cout << "Test case 1 (Original): " << (originalSol.isAnagram(s1, t1) ? "Anagram" : "Not an anagram") << endl;
    cout << "Test case 1 (Optimized): " << (optimizedSol.isAnagram(s1, t1) ? "Anagram" : "Not an anagram") << endl;

    // Test case 2: Not an anagram
    string s2 = "rat";
    string t2 = "car";
    cout << "Test case 2 (Original): " << (originalSol.isAnagram(s2, t2) ? "Anagram" : "Not an anagram") << endl;
    cout << "Test case 2 (Optimized): " << (optimizedSol.isAnagram(s2, t2) ? "Anagram" : "Not an anagram") << endl;

    // Test case 3: Anagram with different characters
    string s3 = "listen";
    string t3 = "silent";
    cout << "Test case 3 (Original): " << (originalSol.isAnagram(s3, t3) ? "Anagram" : "Not an anagram") << endl;
    cout << "Test case 3 (Optimized): " << (optimizedSol.isAnagram(s3, t3) ? "Anagram" : "Not an anagram") << endl;

    return 0;
}
