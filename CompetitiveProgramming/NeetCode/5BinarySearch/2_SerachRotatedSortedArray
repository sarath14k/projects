#include <iostream>
#include <vector>

using namespace std;

class Solution {
public:
    int search(vector<int>& nums, int target) {
        int left = 0;  // Left boundary of the search
        int right = nums.size() - 1;  // Right boundary of the search

        // Binary search loop
        while (left <= right) {
            int mid = left + (right - left) / 2;  // Calculate mid-point to avoid overflow

            // If the target is found at mid
            if (nums[mid] == target) {
                return mid;
            }

            // Determine if the left half is sorted
            if (nums[left] <= nums[mid]) {
                // Check if target is within the sorted left half
                if (nums[left] <= target && target <= nums[mid]) {
                    right = mid - 1;  // Narrow search to the left half
                } else {
                    left = mid + 1;  // Search in the right half
                }
            } 
            // Otherwise, the right half must be sorted
            else {
                // Check if target is within the sorted right half
                if (nums[mid] <= target && target <= nums[right]) {
                    left = mid + 1;  // Narrow search to the right half
                } else {
                    right = mid - 1;  // Search in the left half
                }
            }
        }

        // If the target is not found
        return -1;
    }

    /*
    Time Complexity: O(log n), where n is the number of elements in the array.
    Space Complexity: O(1), as we are using only constant extra space.
    */
};

// Main function to test the solution
int main() {
    Solution solution;

    // Test case
    vector<int> nums = {4, 5, 6, 7, 0, 1, 2};
    int target = 0;

    // Test the search method
    int result = solution.search(nums, target);
    if (result != -1) {
        cout << "Target found at index: " << result << endl;
    } else {
        cout << "Target not found" << endl;
    }

    return 0;
}
