#include <iostream>
#include <vector>
#include <unordered_set>
using namespace std;

// Original Solution class for longest consecutive sequence
class OriginalSolution {
public:
    // Function to find the length of the longest consecutive sequence (original version)
    int longestConsecutive(vector<int>& nums) {
        unordered_set<int> numSet(nums.begin(), nums.end()); // Create a set from the input vector
        int longestLength = 0; // Variable to store the length of the longest consecutive sequence

        // Loop through each number in the set
        for (int num : numSet) {
            // Check if it's the start of a sequence
            if (numSet.find(num - 1) == numSet.end()) {
                int currentLength = 1; // Start length of the current sequence
                // Increment length while the next consecutive number exists
                while (numSet.find(num + currentLength) != numSet.end()) {
                    currentLength++;
                }
                longestLength = max(longestLength, currentLength); // Update longest length if needed
            }
        }
        return longestLength; // Return the length of the longest consecutive sequence
    }
    /*
    Time Complexity: O(n), where n is the number of elements in the input vector, due to the set operations.
    Space Complexity: O(n) for the set used to store the numbers.
    */
};

// Optimized Solution class for longest consecutive sequence
class Solution {
public:
    // Function to find the length of the longest consecutive sequence (optimized version)
    int longestConsecutive(vector<int>& nums) {
        unordered_set<int> numSet(nums.begin(), nums.end()); // Create a set from the input vector
        int longestLength = 0; // Variable to store the length of the longest consecutive sequence

        // Loop through each number in the set
        for (int num : numSet) {
            // Only start counting if it's the beginning of a sequence
            if (numSet.find(num - 1) == numSet.end()) {
                int currentLength = 1; // Start length of the current sequence
                // Increment length while the next consecutive number exists
                while (numSet.find(num + currentLength) != numSet.end()) {
                    currentLength++;
                }
                longestLength = max(longestLength, currentLength); // Update longest length if needed
            }
        }
        return longestLength; // Return the length of the longest consecutive sequence
    }
    /*
    Time Complexity: O(n), where n is the number of elements in the input vector, due to the set operations.
    Space Complexity: O(n) for the set used to store the numbers.
    */
};

// Simple main function to test both versions
int main() {
    OriginalSolution originalSol;
    Solution optimizedSol;

    // Test case: Example input
    vector<int> nums = {100, 4, 200, 1, 3, 2};

    // Test the original solution
    int originalResult = originalSol.longestConsecutive(nums);
    cout << "Original Solution Result: " << originalResult << endl;

    // Test the optimized solution
    int optimizedResult = optimizedSol.longestConsecutive(nums);
    cout << "Optimized Solution Result: " << optimizedResult << endl;

    return 0;
}
