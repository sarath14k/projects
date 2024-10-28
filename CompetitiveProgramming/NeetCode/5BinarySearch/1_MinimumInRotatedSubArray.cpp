#include <iostream>
#include <vector>
#include <algorithm>  // For min function

using namespace std;

class Solution {
public:
    int findMin(vector<int>& nums) {
        int minimumValue = nums[0];  // Initialize with the first element as the minimum
        int left = 0;  // Left pointer
        int right = nums.size() - 1;  // Right pointer

        // Binary search to find the minimum in the rotated sorted array
        while (left <= right) {
            // If the subarray is already sorted, return the minimum element
            if (nums[left] < nums[right]) {
                minimumValue = min(minimumValue, nums[left]);
                break;
            }

            // Calculate the mid-point
            int mid = left + (right - left) / 2;
            minimumValue = min(minimumValue, nums[mid]);

            // If the mid element is greater than or equal to the left, the minimum is on the right
            if (nums[mid] >= nums[left]) {
                left = mid + 1;  // Move left pointer to the right of mid
            }
            // If the mid element is less than the left, the minimum is on the left side
            else {
                right = mid - 1;  // Move right pointer to the left of mid
            }
        }

        return minimumValue;  // Return the minimum element found
    }

    /*
    Time Complexity: O(log n), where n is the number of elements in the array due to binary search.
    Space Complexity: O(1), as we are using only constant extra space.
    */
};

// Main function to test the solution
int main() {
    Solution solution;

    // Test case
    vector<int> nums = {4, 5, 6, 7, 0, 1, 2};

    // Test the findMin method
    int result = solution.findMin(nums);
    cout << "The minimum value in the rotated sorted array is: " << result << endl;

    return 0;
}
