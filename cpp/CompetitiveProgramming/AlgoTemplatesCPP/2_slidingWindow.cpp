#include <iostream>
#include <vector>
#include <unordered_map> // For frequency counting

void slidingWindowAlgorithm(const std::string& s, int k) {
    std::unordered_map<char, int> charCount; // To keep track of character counts
    int left = 0; // Initialize left pointer
    int maxLength = 0; // To store the maximum length found

    // Expand the right pointer
    for (int right = 0; right < s.size(); ++right) {
        charCount[s[right]]++; // Include the character at the right pointer

        // Shrink the window if the condition is violated
        while (charCount.size() > k) { // Example condition: more than k unique characters
            charCount[s[left]]--; // Remove character at left pointer
            if (charCount[s[left]] == 0) {
                charCount.erase(s[left]); // Remove the character if its count is zero
            }
            left++; // Move the left pointer to shrink the window
        }

        // Update maximum length if needed
        maxLength = std::max(maxLength, right - left + 1);
    }

    std::cout << "Maximum length of substring with at most " << k << " unique characters: " << maxLength << std::endl;
}

int main() {
    // Example usage
    std::string s = "abcabcbb"; // Input string
    int k = 2; // Example number of unique characters

    slidingWindowAlgorithm(s, k);

    return 0;
}
