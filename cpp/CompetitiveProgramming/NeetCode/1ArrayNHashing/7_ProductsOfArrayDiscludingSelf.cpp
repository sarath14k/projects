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
