#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
using namespace std;

// Original Solution class to group anagrams
class OriginalSolution {
public:
    // Function to group anagrams together (original version)
    vector<vector<string>> groupAnagrams(vector<string>& words) {
        unordered_map<string, vector<string>> anagramGroups;  // Map to store sorted words as keys and corresponding anagrams as values

        // Loop through each word in the input vector
        for (const auto& word : words) {
            string sortedWord = word;  // Copy the word to sort it
            sort(sortedWord.begin(), sortedWord.end());  // Sort the word to find anagrams
            anagramGroups[sortedWord].push_back(word);  // Add the original word to the map using the sorted word as the key
        }

        // Collect all the anagram groups into a result vector
        vector<vector<string>> groupedAnagrams;
        for (const auto& group : anagramGroups) {
            groupedAnagrams.push_back(group.second);  // Add each group of anagrams to the result
        }

        return groupedAnagrams;  // Return the grouped anagrams
    }
    /*
    Time Complexity: O(n * k log k), where n is the number of words and k is the maximum length of a word.
    Space Complexity: O(n * k), where n is the number of words and k is the maximum length of a word due to the storage of the anagrams.
    */
};

// Optimized Solution class to group anagrams
class Solution {
public:
    // Function to group anagrams together (optimized version)
    vector<vector<string>> groupAnagrams(vector<string>& words) {
        unordered_map<string, vector<string>> anagramGroups;  
        anagramGroups.reserve(words.size());  // Improvement: Reserve space for the map to avoid multiple reallocations

        // Loop through each word in the input vector
        for (auto& word : words) {
            string sortedWord = word;  // Same as original: Copy the word
            sort(sortedWord.begin(), sortedWord.end());  // Same as original: Sort the word to find anagrams
            anagramGroups[move(sortedWord)].push_back(move(word));  // Improvement: Use move semantics to avoid unnecessary deep copying
        }

        // Improvement: Reserve space for the result vector to avoid reallocations
        vector<vector<string>> groupedAnagrams;
        groupedAnagrams.reserve(anagramGroups.size());  // Reserve space based on the number of anagram groups

        // Loop to collect the groups
        for (auto& group : anagramGroups) {
            groupedAnagrams.push_back(move(group.second));  // Improvement: Use move semantics to avoid copying vectors of strings
        }

        return groupedAnagrams;  // Return the grouped anagrams
    }
    /*
    Time Complexity: O(n * k log k), where n is the number of words and k is the maximum length of a word.
    Space Complexity: O(n * k), where n is the number of words and k is the maximum length of a word due to the storage of the anagrams.
    */
};

// Simple main function to test both versions
int main() {
    // Create instances of both Original and Optimized Solution classes
    OriginalSolution originalSol;
    Solution optimizedSol;  // Using just "Solution" for the optimized version

    // Test case: Simple example
    vector<string> words = {"eat", "tea", "tan", "ate", "nat", "bat"};

    // Test the original solution
    cout << "Original Solution: Grouped anagrams:" << endl;
    vector<vector<string>> result1 = originalSol.groupAnagrams(words);
    for (const auto& group : result1) {
        for (const auto& word : group) {
            cout << word << " ";
        }
        cout << endl;
    }

    // Reset the input data as it was modified by the optimized version
    words = {"eat", "tea", "tan", "ate", "nat", "bat"};

    // Test the optimized solution
    cout << "Optimized Solution: Grouped anagrams:" << endl;
    vector<vector<string>> result2 = optimizedSol.groupAnagrams(words);
    for (const auto& group : result2) {
        for (const auto& word : group) {
            cout << word << " ";
        }
        cout << endl;
    }

    return 0;
}
