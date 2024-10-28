#include <iostream>
#include <vector>
using namespace std;

// Original Solution class for product except self
class OriginalSolution {
public:
    // Function to compute the product of elements except self (original version)
    vector<int> productExceptSelf(vector<int>& nums) {
        int size = nums.size(); // Get the size of the input vector
        vector<int> result(size); // Vector to store the result

        // Loop through each element in nums
        for (int i = 0; i < size; i++) {
            int product = 1; // Variable to hold the product for the current index
            for (int j = 0; j < size; j++) {
                if (i != j) { // Skip the current index
                    product *= nums[j]; // Multiply other elements
                }
            }
            result[i] = product; // Store the product in the result vector
        }
        return result; // Return the result vector
    }
    /*
    Time Complexity: O(n^2), where n is the number of elements in the input vector.
    Space Complexity: O(n) for the result vector.
    */
};

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
    OriginalSolution originalSol;
    Solution optimizedSol;

    // Test case: Example input
    vector<int> nums = {1, 2, 3, 4};

    // Test the original solution
    vector<int> originalResult = originalSol.productExceptSelf(nums);
    cout << "Original Solution Result: ";
    for (int value : originalResult) {
        cout << value << " ";
    }
    cout << endl;

    // Test the optimized solution
    vector<int> optimizedResult = optimizedSol.productExceptSelf(nums);
    cout << "Optimized Solution Result: ";
    for (int value : optimizedResult) {
        cout << value << " ";
    }
    cout << endl;

    return 0;
}
