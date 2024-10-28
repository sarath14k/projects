#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Merged Solution class for maxProfit
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int maxProfit = 0;  // Variable to store the maximum profit
        int buyIndex = 0;   // Pointer for the buying price
        int sellIndex = 0;  // Pointer for the selling price
        
        // Iterate through the prices
        while (sellIndex < prices.size()) {
            // If current selling price is greater than the buying price
            if (prices[sellIndex] > prices[buyIndex]) {
                // Update maxProfit if the current profit is greater
                maxProfit = max(maxProfit, prices[sellIndex] - prices[buyIndex]);
            } else {
                // Update the buying index to the current selling index
                buyIndex = sellIndex;
            }
            // Move to the next price
            ++sellIndex;
        }
        return maxProfit;  // Return the maximum profit found
    }
    /*
    Time Complexity: O(n), where n is the number of elements in prices.
    Space Complexity: O(1), as we are using only a constant amount of space.
    */
};

// Main function to test the solution
int main() {
    Solution solution;

    // Test case
    vector<int> prices = {7, 1, 5, 3, 6, 4};

    // Test the maxProfit method
    int result = solution.maxProfit(prices);
    cout << "Maximum profit that can be achieved: " << result << endl;

    return 0;
}
