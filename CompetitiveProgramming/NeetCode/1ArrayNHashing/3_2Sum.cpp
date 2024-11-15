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
