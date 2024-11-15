#include <iostream>
#include <vector>
using namespace std;

int findPeakElement(const vector<int>& nums) {
    int n = nums.size();
    for (int i = 0; i < n; i++) {
        // Check if nums[i] is a peak element
        if ((i == 0 || nums[i] >= nums[i - 1]) && (i == n - 1 || nums[i] >= nums[i + 1])) {
            return i;
        }
    }
    return -1; // No peak element found
}

int main() {
    vector<int> nums = {1, 2, 3, 1}; // Example array
    int peakIndex = findPeakElement(nums);
    if (peakIndex != -1) {
        cout << "Peak element found at index " << peakIndex << ": " << nums[peakIndex] << endl;
    } else {
        cout << "No peak element found in the array." << endl;
    }
    return 0;
}
