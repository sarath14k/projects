#include <iostream>
#include <vector>
#include <unordered_set>
using namespace std;

// Original Solution class to check if a vector contains duplicate elements
class Solution{
    public:
        bool containsDuplicate(vector<int>& nums){
            unordered_set<int> st;
            for(int num: nums){
                if(st.count(num))
                    return true;
                st.insert(num);
            }
            return false;
        }
};

/*
 * =======================================================
 * DEBUGGER TRACE (Visualizing Test Case 1: nums = {1, 2, 3, 1})
 * =======================================================
 * Init: st = empty {}
 * 
 * Iteration 1: num = 1
 *   - st.count(1) == false.
 *   - st.insert(1) -> st is now {1}
 * 
 * Iteration 2: num = 2
 *   - st.count(2) == false.
 *   - st.insert(2) -> st is now {1, 2}
 * 
 * Iteration 3: num = 3
 *   - st.count(3) == false.
 *   - st.insert(3) -> st is now {1, 2, 3}
 * 
 * Iteration 4: num = 1
 *   - st.count(1) == TRUE! (Because 1 is already in the set)
 *   - return true! -> Exits early, duplicate found.
 * 
 * Time Complexity: O(N) - We iterate through the array at most once.
 * Space Complexity: O(N) - In the worst case (no duplicates), we store all N elements in the hash set.
 * =======================================================
 */

// Simple main function to test both versions
int main() {
    // Create instances of both Original and Optimized Solution classes
    Solution optimizedSol;  // Using just "Solution" for the optimized version

    // Test case 1: Contains duplicates
    vector<int> nums1 = {1, 2, 3, 1};
    cout << "Test case 1 (Optimized): " << (optimizedSol.containsDuplicate(nums1) ? "Contains duplicates" : "No duplicates") << endl;

    // Test case 2: No duplicates
    vector<int> nums2 = {1, 2, 3, 4};
    cout << "Test case 2 (Optimized): " << (optimizedSol.containsDuplicate(nums2) ? "Contains duplicates" : "No duplicates") << endl;

    // Test case 3: Contains duplicates
    vector<int> nums3 = {1, 1, 1, 3, 3, 4, 2, 2};
    cout << "Test case 3 (Optimized): " << (optimizedSol.containsDuplicate(nums3) ? "Contains duplicates" : "No duplicates") << endl;

    return 0;
}
