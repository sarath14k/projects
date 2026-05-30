#include <unordered_map>
#include <vector>
#include <iostream>

using namespace std;

class Solution{
    public:
        vector<int> twoSum(vector<int>&, int&);
};
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> mp;
    mp.reserve(nums.size());
    int i = 0, complement;
    for(int num : nums){
        complement = target - num;
        auto it = mp.find(complement);
        if(it != mp.end())
            return {it->second, i};
        mp[num] = i;
        ++i;
    }
    return {};
}
/*
 * =======================================================
 * DEBUGGER TRACE (Visualizing Test Case: nums = {2, 7, 10, 15, 11, 14, 18}, target = 26)
 * =======================================================
 * Init: unordered_map mp = empty {}, i = 0
 * 
 * Iteration 1: num = 2, i = 0
 *   - complement = 26 - 2 = 24
 *   - mp.find(24) ? NOT FOUND.
 *   - mp[2] = 0.   -> mp is now { {2: 0} }
 * 
 * Iteration 2: num = 7, i = 1
 *   - complement = 26 - 7 = 19
 *   - mp.find(19) ? NOT FOUND.
 *   - mp[7] = 1.   -> mp is now { {2: 0}, {7: 1} }
 * 
 * Iteration 3: num = 10, i = 2
 *   - complement = 26 - 10 = 16
 *   - mp.find(16) ? NOT FOUND.
 *   - mp[10] = 2.  -> mp is now { {2: 0}, {7: 1}, {10: 2} }
 * 
 * Iteration 4: num = 15, i = 3
 *   - complement = 26 - 15 = 11
 *   - mp.find(11) ? NOT FOUND.
 *   - mp[15] = 3.  -> mp is now { ..., {15: 3} }
 * 
 * Iteration 5: num = 11, i = 4
 *   - complement = 26 - 11 = 15
 *   - mp.find(15) ? FOUND! (15 was seen at index 3)
 *   - return {3, 4}! -> Exits early, pair found.
 * 
 * Time Complexity: O(N) - We iterate through the array exactly once.
 * Space Complexity: O(N) - We store at most N elements in the hash map.
 * =======================================================
 */

int main()
{
    Solution obj;
    vector<int> num = {2, 7, 10, 15, 11, 14, 18};
    int target = 26;
    vector<int> result = obj.twoSum(num, target);
    cout << "Indices = [" << result[0] << ", " << result[1] << "]\n";
    return 0;
}

//O(n)
