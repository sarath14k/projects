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
