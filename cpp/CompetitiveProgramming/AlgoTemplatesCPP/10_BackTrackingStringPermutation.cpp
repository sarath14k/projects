#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

void backtrack(std::string& s, int start, std::vector<std::string>& results) {
    if (start == s.size() - 1) {
        results.push_back(s); // Found a valid permutation
        return;
    }

    for (int i = start; i < s.size(); ++i) {
        std::swap(s[start], s[i]); // Swap to create a new permutation
        backtrack(s, start + 1, results); // Recur
        std::swap(s[start], s[i]); // Backtrack: revert to original configuration
    }
}

int main() {
    std::string s = "abc"; // Input string
    std::vector<std::string> results;

    backtrack(s, 0, results);

    std::cout << "Permutations of " << s << ":\n";
    for (const auto& perm : results) {
        std::cout << perm << std::endl;
    }

    return 0;
}
