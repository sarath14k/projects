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
