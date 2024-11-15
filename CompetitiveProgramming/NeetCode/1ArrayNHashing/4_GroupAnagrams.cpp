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
