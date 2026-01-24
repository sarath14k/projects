#include <iostream>
#include <unordered_map>
#include <string>
using namespace std;

// Original Solution class to check if two strings are anagrams
class Solution {
public:
    bool isAnagram(string s, string t) {
        if(s.size() != t.size())
            return false;
        unordered_map<char, int> charCount;
        for(char c : s)
            charCount[c]++;
        for(char c : t)
            if(charCount[c]-- == 0)
                return false;
        return true;
    }
};

// Simple main function to test both versions
int main() {
    Solution optimizedSol;  // Using just "Solution" for the optimized version

    // Test case 1: Anagram
    string s1 = "anagram";
    string t1 = "nagaram";
    cout << "Test case 1 (Optimized): " << (optimizedSol.isAnagram(s1, t1) ? "Anagram" : "Not an anagram") << endl;

    // Test case 2: Not an anagram
    string s2 = "rat";
    string t2 = "car";
    cout << "Test case 2 (Optimized): " << (optimizedSol.isAnagram(s2, t2) ? "Anagram" : "Not an anagram") << endl;

    // Test case 3: Anagram with different characters
    string s3 = "listen";
    string t3 = "silent";
    cout << "Test case 3 (Optimized): " << (optimizedSol.isAnagram(s3, t3) ? "Anagram" : "Not an anagram") << endl;

    return 0;
}
