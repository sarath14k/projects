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

int main()
{
    vector<int> nums = {4,2,100,3,12,1};
    int result = longestConsecutive(nums);
    cout << "Longest sequence length => " << result << endl;
}
