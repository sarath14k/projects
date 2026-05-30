#include <iostream>
#include <vector>
#include <unordered_set>
using namespace std;

int longestConsecutive(vector<int>& nums){
    unordered_set<int> num_set(nums.begin(), nums.end());
    int longest = 0;
    for(int num : nums){
        if(!num_set.count(num - 1)){
            int length = 1;
            while(num_set.count(num + length))
                  length++;
            longest = max(longest, length);
        }
    }
    return longest;
}

/*
 * =======================================================
 * DEBUGGER TRACE (Visualizing Test Case: nums = {4, 2, 100, 3, 12, 1})
 * =======================================================
 * Init: num_set = {4, 2, 100, 3, 12, 1}
 * 
 * Loop over nums:
 *   - num = 4: num_set.count(3) is TRUE. Not the start of a sequence. Skip.
 *   - num = 2: num_set.count(1) is TRUE. Not the start. Skip.
 * 
 *   - num = 100: num_set.count(99) is FALSE! (Start of sequence)
 *       - count(101) is FALSE. length = 1. longest = max(0, 1) = 1
 * 
 *   - num = 3: num_set.count(2) is TRUE. Not the start. Skip.
 * 
 *   - num = 12: num_set.count(11) is FALSE! (Start of sequence)
 *       - count(13) is FALSE. length = 1. longest = max(1, 1) = 1
 * 
 *   - num = 1: num_set.count(0) is FALSE! (Start of sequence)
 *       - count(2) is TRUE! length = 2
 *       - count(3) is TRUE! length = 3
 *       - count(4) is TRUE! length = 4
 *       - count(5) is FALSE. length stops at 4.
 *       - longest = max(1, 4) = 4.
 * 
 * Final Result: 4 (The sequence is 1 -> 2 -> 3 -> 4)
 * 
 * Time Complexity: O(N) - Building the set takes O(N). Then we only loop over a sequence if it's the start, making it O(N) overall.
 * Space Complexity: O(N) - The hash set stores all N elements.
 * =======================================================
 */

int main()
{
    vector<int> nums = {4,2,100,3,12,1};
    int result = longestConsecutive(nums);
    cout << "Longest sequence length => " << result << endl;
}
