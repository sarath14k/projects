#include <iostream>
#include <vector>
#include <algorithm> // For std::sort if needed

void twoPointerAlgorithm(const std::vector<int>& nums) {
    int left = 0;                      // Initialize left pointer
    int right = nums.size() - 1;      // Initialize right pointer

    // Loop until the two pointers meet
    while (left < right) {
        // Example condition: find a pair that sums to a target
        int sum = nums[left] + nums[right];

        // Replace 'target' with the desired sum
        if (sum == target) {
            std::cout << "Pair found: (" << nums[left] << ", " << nums[right] << ")\n";
            // Optionally move pointers or perform other operations
            left++;
            right--;
        } else if (sum < target) {
            left++;  // Move left pointer to the right to increase the sum
        } else {
            right--; // Move right pointer to the left to decrease the sum
        }
    }
}

int main() {
    // Example usage
    std::vector<int> nums = {1, 2, 3, 4, 5};
    int target = 6; // Example target sum

    // You may need to sort the array if it's not sorted
    std::sort(nums.begin(), nums.end());

    twoPointerAlgorithm(nums);

    return 0;
}
