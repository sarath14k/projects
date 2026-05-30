#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>

using namespace std;

class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> anagrams;

        for (string word : strs) {
            vector<int> count(26, 0);
            for (char c : word)
                count[c - 'a']++;
            string key;
            for (int freq : count)
                key += to_string(freq) + '#';
            anagrams[key].emplace_back(word);
        }

        vector<vector<string>> result;
        for (auto& group : anagrams)
            result.emplace_back(group.second);


        return result;
    }
};

/*
 * =======================================================
 * DEBUGGER TRACE (Visualizing word processing for "bat", "tan", "nat"...)
 * =======================================================
 * Init: unordered_map<string, vector<string>> anagrams = empty {}
 * 
 * Iteration 1: word = "bat"
 *   - Build count array for "bat" (1 'a', 1 'b', 1 't')
 *   - Generate unique string key: "1#1#0#0...1#..."
 *   - anagrams["1#1#...1#"].emplace_back("bat")
 * 
 * Iteration 2: word = "tan"
 *   - Build count array for "tan" (1 'a', 1 'n', 1 't')
 *   - Generate unique string key: "1#0#...1#...1#..."
 *   - anagrams["1#0#...1#"].emplace_back("tan")
 * 
 * Iteration 3: word = "nat"
 *   - Build count array for "nat" (1 'a', 1 'n', 1 't')
 *   - Generate unique string key: "1#0#...1#...1#..." 
 *     -> (NOTICE: EXACT SAME KEY AS "tan"!)
 *   - anagrams["1#0#...1#"].emplace_back("nat")
 *     -> Now map holds: { "1#0#...1#" : ["tan", "nat"] }
 * 
 * Result: All words with identical character frequencies map to the 
 * exact same hashmap key, grouping them automatically!
 * 
 * Time Complexity: O(N * M) - N is number of words, M is max length of a word.
 * Space Complexity: O(N * M) - To store the keys and the final grouped arrays.
 * =======================================================
 */

int main() {
    vector<string> words = {"bat", "tan", "nat", "eat", "tea", "ate"};
    Solution obj;
    vector<vector<string>> result = obj.groupAnagrams(words);

    cout << "Grouped Anagrams:\n";
    for (const auto& group : result) {
        for (const string& word : group) {
            cout << word << " ";
        }
        cout << endl;
    }
    return 0;
}
