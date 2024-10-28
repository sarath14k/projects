#include <iostream>
#include <vector>
#include <unordered_set>
using namespace std;

// Original Solution class to check if a vector contains duplicate elements
class OriginalSolution {
public:
    // Function to determine if a vector contains any duplicates
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> st; // Unordered set to store unique elements
        // Loop through each element in the vector
        for(int i = 0; i < nums.size(); i++) {
            // If the element is found in the set, return true (duplicate found)
            if(st.find(nums[i]) != st.end()) 
                return true;
            // Insert the current element into the set
            st.insert(nums[i]);
        }
        // If no duplicates are found, return false
        return false;
    }
    /*
    Time Complexity: O(n) where n is the number of elements in the vector,
    since we may need to insert all elements into the set in the worst case.
    Space Complexity: O(n) for the unordered set to store unique elements.
    */
};

// Optimized Solution class to check if a vector contains duplicate elements
class Solution {
public:
    // Optimized function to determine if a vector contains any duplicates
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> st; // Unordered set to store unique elements
        // Loop through each element in the vector
        for (int num : nums) {
            // If the element is found in the set, return true (duplicate found)
            if (!st.insert(num).second)  // Insert and check if insertion was successful
                return true;  // Duplicate found
        }
        // If no duplicates are found, return false
        return false;
    }
    /*
    Time Complexity: O(n) where n is the number of elements in the vector,
    since we may need to insert all elements into the set in the worst case.
    Space Complexity: O(n) for the unordered set to store unique elements.
    */
};

// Simple main function to test both versions
int main() {
    // Create instances of both Original and Optimized Solution classes
    OriginalSolution originalSol;
    Solution optimizedSol;  // Using just "Solution" for the optimized version

    // Test case 1: Contains duplicates
    vector<int> nums1 = {1, 2, 3, 1}; 
    cout << "Test case 1 (Original): " << (originalSol.containsDuplicate(nums1) ? "Contains duplicates" : "No duplicates") << endl;
    cout << "Test case 1 (Optimized): " << (optimizedSol.containsDuplicate(nums1) ? "Contains duplicates" : "No duplicates") << endl;

    // Test case 2: No duplicates
    vector<int> nums2 = {1, 2, 3, 4}; 
    cout << "Test case 2 (Original): " << (originalSol.containsDuplicate(nums2) ? "Contains duplicates" : "No duplicates") << endl;
    cout << "Test case 2 (Optimized): " << (optimizedSol.containsDuplicate(nums2) ? "Contains duplicates" : "No duplicates") << endl;

    // Test case 3: Contains duplicates
    vector<int> nums3 = {1, 1, 1, 3, 3, 4, 2, 2}; 
    cout << "Test case 3 (Original): " << (originalSol.containsDuplicate(nums3) ? "Contains duplicates" : "No duplicates") << endl;
    cout << "Test case 3 (Optimized): " << (optimizedSol.containsDuplicate(nums3) ? "Contains duplicates" : "No duplicates") << endl;

    return 0;
}
