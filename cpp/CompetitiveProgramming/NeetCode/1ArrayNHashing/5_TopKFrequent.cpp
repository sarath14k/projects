#include <iostream>
#include <vector>
#include <unordered_map>

using namespace std;

class Solution{
    public:
        vector<pair<int, int>> topKFrequent(vector<int>& nums, const int& k);
};

vector<pair<int, int>> Solution::topKFrequent(vector<int>& nums, const int& k){
    unordered_map <int, int> freqMap;
    vector <vector<int>> freq(nums.size()+1);

    for(int num : nums)
        freqMap[num]++;

    for(auto& itr : freqMap)
        freq[itr.second].emplace_back(itr.first);

    vector <pair<int,int>> result;
    result.reserve(k);

    for(int i = freq.size() - 1; i > 0 && result.size() < k; --i)
        for(int num : freq[i]){
            result.emplace_back(num, i);
            if(result.size() == k)
                break;
        }

    return result;
}
/*
 * =======================================================
 * DEBUGGER TRACE (Visualizing Top K Frequent for {1,1,1,2,2,2,3,3,4,4,4,4,5}, k=6)
 * =======================================================
 * Init: freqMap = {}, freq array (buckets) size = 14
 * 
 * Step 1 (Count Frequencies):
 *   - freqMap = { {1:3}, {2:3}, {3:2}, {4:4}, {5:1} }
 * 
 * Step 2 (Bucket Sort - placing into freq array by count):
 *   - freq[4] = {4}      (number '4' appeared 4 times)
 *   - freq[3] = {1, 2}   (numbers '1' and '2' appeared 3 times)
 *   - freq[2] = {3}      (number '3' appeared 2 times)
 *   - freq[1] = {5}      (number '5' appeared 1 time)
 * 
 * Step 3 (Gather top elements from right to left, i.e., highest frequency first):
 *   - i = 13..5: Empty buckets.
 *   - i = 4: found {4}. result = { (4, freq 4) }
 *   - i = 3: found {1, 2}. result = { ..., (1, freq 3), (2, freq 3) }
 *   - i = 2: found {3}. result = { ..., (3, freq 2) }
 *   - i = 1: found {5}. result = { ..., (5, freq 1) }
 * 
 * Result size is 5 (since we ran out of unique numbers before hitting k=6)
 * 
 * Time Complexity: O(N) - We count frequencies O(N), put them in buckets O(N), and read buckets O(N).
 * Space Complexity: O(N) - The hash map and the bucket array both store at most N elements.
 * =======================================================
 */

int main()
{
    vector<int> nums = {1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5};
    int k = 6;
    cout << "\n***TOP " << k << " FREQUENT***\n";
    Solution obj;
    vector<pair<int, int>> result = obj.topKFrequent(nums, k);

    for(const auto& pair : result)
        cout << pair.first << " => " << pair.second << '\n';
    return 0;
}
