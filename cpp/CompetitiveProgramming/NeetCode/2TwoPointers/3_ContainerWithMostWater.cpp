#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Merged Solution class for maxArea
class Solution {
public:
    int maxArea(vector<int>& heights) {
        int left = 0;  // Left pointer
        int right = heights.size() - 1;  // Right pointer
        int maxArea = 0;  // Variable to store the maximum area

        // While left pointer is less than right pointer
        while (left < right) {
            // Calculate area with the current left and right pointers
            int area = min(heights[left], heights[right]) * (right - left);
            maxArea = max(maxArea, area);  // Update max area if current area is larger

            // Move the pointer pointing to the shorter line
            if (heights[left] <= heights[right])
                left++;
            else
                right--;

        }
        return maxArea;  // Return the maximum area found
    }
    /*
    Time Complexity: O(n), where n is the number of elements in heights.
    Space Complexity: O(1), as we are using only a constant amount of space.
    */
};

// Main function to test the solution
int main() {
    Solution solution;

    // Test case
    vector<int> heights = {1, 8, 6, 2, 5, 4, 8, 3, 7};

    // Test the maxArea method
    int result = solution.maxArea(heights);
    cout << "Maximum area of water that can be trapped: " << result << endl;

    return 0;
}
