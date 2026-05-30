#include <iostream>
#include <vector>
using namespace std;

// Optimized Solution class for product except self
class Solution {
public:
    // Function to compute the product of elements except self (optimized version)
    vector<int> productExceptSelf(vector<int>& nums) {
        int size = nums.size(); // Get the size of the input vector
        vector<int> result(size, 1); // Vector to store the result initialized to 1

        // Compute the prefix products
        for (int i = 1; i < size; i++) {
            result[i] = result[i - 1] * nums[i - 1]; // Multiply by previous prefix product
        }

        // Compute the postfix products and multiply with the result
        int postfixProduct = 1; // Variable to hold the postfix product
        for (int i = size - 1; i >= 0; i--) {
            result[i] *= postfixProduct; // Multiply the result by the current postfix product
            postfixProduct *= nums[i]; // Update postfix product for the next iteration
        }
        return result; // Return the result vector
    }
    /*
    Time Complexity: O(n), where n is the number of elements in the input vector.
    Space Complexity: O(n) for the result vector.
    */
};

/*
 * =======================================================
 * DEBUGGER TRACE (Visualizing nums = {1, 2, 3, 4})
 * =======================================================
 * Init: result = {1, 1, 1, 1}
 * 
 * PASS 1: Prefix Products (Left to Right)
 *   - i = 1: result[1] = result[0]*nums[0] = 1 * 1 = 1  -> {1, 1, 1, 1}
 *   - i = 2: result[2] = result[1]*nums[1] = 1 * 2 = 2  -> {1, 1, 2, 1}
 *   - i = 3: result[3] = result[2]*nums[2] = 2 * 3 = 6  -> {1, 1, 2, 6}
 * 
 * PASS 2: Postfix Products (Right to Left)
 *   - Init: postfixProduct = 1
 *   - i = 3: result[3] *= 1 (6),   postfixProduct *= nums[3] (4) = 4
 *   - i = 2: result[2] *= 4 (8),   postfixProduct *= nums[2] (3) = 12
 *   - i = 1: result[1] *= 12 (12), postfixProduct *= nums[1] (2) = 24
 *   - i = 0: result[0] *= 24 (24), postfixProduct *= nums[0] (1) = 24
 * 
 * Final Result: {24, 12, 8, 6}
 * =======================================================
 */

// Simple main function to test both versions
int main() {
    Solution optimizedSol;

    // Test case: Example input
    vector<int> nums = {1, 2, 3, 4};

    // Test the optimized solution
    vector<int> optimizedResult = optimizedSol.productExceptSelf(nums);
    cout << "Optimized Solution Result: ";
    for (int value : optimizedResult) {
        cout << value << " ";
    }
    cout << endl;

    return 0;
}
