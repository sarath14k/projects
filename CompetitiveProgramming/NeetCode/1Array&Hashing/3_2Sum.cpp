#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

// Solution class to find two indices such that the sum equals the target
class Solution {
public:
    // Function to find two indices in nums that add up to the target
    vector<int> twoSum(vector<int>& nums, int target) {
        int n = nums.size();  // Get the size of the input vector
        unordered_map<int, int> mp;  // Map to store the element and its index
        mp.reserve(n);  // Reserve space for the expected number of elements

        // Loop through the elements of the vector
        for (int i = 0; i < n; ++i) {
            int complement = target - nums[i];  // Calculate the complement

            // Check if the complement exists in the map
            if (auto it = mp.find(complement); it != mp.end()) {  // C++17 if-with-initializer
                return {it->second, i};  // Return the indices if found
            }

            // Store the current element and its index in the map
            mp[nums[i]] = i;
        }
        return {};  // Return an empty vector if no solution is found
    }
};

// Simple main function to test the twoSum method
int main() {
    // Create an instance of the Solution class
    Solution sol;

    // Test case 1: Simple example
    vector<int> nums1 = {2, 7, 11, 15};
    int target1 = 9;
    vector<int> result1 = sol.twoSum(nums1, target1);
    cout << "Test case 1: Indices = [" << result1[0] << ", " << result1[1] << "]" << endl;

    // Test case 2: Another example
    vector<int> nums2 = {3, 2, 4};
    int target2 = 6;
    vector<int> result2 = sol.twoSum(nums2, target2);
    cout << "Test case 2: Indices = [" << result2[0] << ", " << result2[1] << "]" << endl;

    // Test case 3: Different target
    vector<int> nums3 = {3, 3};
    int target3 = 6;
    vector<int> result3 = sol.twoSum(nums3, target3);
    cout << "Test case 3: Indices = [" << result3[0] << ", " << result3[1] << "]" << endl;

    return 0;
}
