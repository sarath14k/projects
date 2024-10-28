#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Original Solution class for threeSum
class OriginalSolution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> res;

        for (int i = 0; i < nums.size(); i++) {
            if (nums[i] > 0) break;  // If the current number is positive, no need to continue
            if (i > 0 && nums[i] == nums[i - 1]) continue;  // Skip duplicates

            int l = i + 1, r = nums.size() - 1;  // Initialize left and right pointers
            while (l < r) {
                int sum = nums[i] + nums[l] + nums[r];  // Calculate the sum
                if (sum > 0) {
                    r--;  // Move right pointer to the left
                } else if (sum < 0) {
                    l++;  // Move left pointer to the right
                } else {
                    res.push_back({nums[i], nums[l], nums[r]});  // Found a triplet
                    l++; r--;
                    while (l < r && nums[l] == nums[l - 1]) {
                        l++;  // Skip duplicates
                    }
                }
            }
        }
        return res;  // Return the list of triplets
    }
    /*
    Time Complexity: O(n^2), where n is the number of elements in nums.
    Space Complexity: O(k), where k is the number of triplets.
    */
};

// Optimized Solution class for threeSum
class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());  // Sort the input array
        vector<vector<int>> res;  // Resultant list of triplets

        for (int i = 0; i < nums.size(); i++) {
            if (nums[i] > 0) break;  // Stop if current number is greater than 0
            if (i > 0 && nums[i] == nums[i - 1]) continue;  // Skip duplicates

            int l = i + 1, r = nums.size() - 1;  // Initialize left and right pointers
            while (l < r) {
                int sum = nums[i] + nums[l] + nums[r];  // Calculate the sum
                if (sum > 0) {
                    r--;  // Move right pointer to the left
                } else if (sum < 0) {
                    l++;  // Move left pointer to the right
                } else {
                    res.push_back({nums[i], nums[l], nums[r]});  // Found a triplet
                    l++; r--;
                    while (l < r && nums[l] == nums[l - 1]) {
                        l++;  // Skip duplicates
                    }
                }
            }
        }
        return res;  // Return the list of triplets
    }
    /*
    Time Complexity: O(n^2), where n is the number of elements in nums.
    Space Complexity: O(k), where k is the number of triplets.
    */
};

// Main function to test both solutions
int main() {
    OriginalSolution originalSol;
    Solution optimizedSol;

    // Test case
    vector<int> nums = {-1, 0, 1, 2, -1, -4};

    // Test the original solution
    cout << "Original Solution: " << endl;
    vector<vector<int>> result1 = originalSol.threeSum(nums);
    for (const auto& triplet : result1) {
        cout << "[";
        for (const auto& num : triplet) {
            cout << num << " ";
        }
        cout << "]" << endl;
    }

    // Test the optimized solution
    cout << "Optimized Solution: " << endl;
    vector<vector<int>> result2 = optimizedSol.threeSum(nums);
    for (const auto& triplet : result2) {
        cout << "[";
        for (const auto& num : triplet) {
            cout << num << " ";
        }
        cout << "]" << endl;
    }

    return 0;
}
