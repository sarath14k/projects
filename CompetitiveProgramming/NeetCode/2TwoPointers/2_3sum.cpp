#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

vector<vector<int>> threeSum(vector<int>& nums){
    sort(nums.begin(), nums.end());
    vector<vector<int>> res;
    for(int i = 0; i < nums.size(); i++){
        if(nums[i] > 0) break;
        if(i > 0 && nums[i] == nums[i - 1]) continue;
        int l = i + 1, r = nums.size() - 1;
        while(l < r){
            int sum = nums[i] + nums[l]+ nums[r];
            if(sum == 0){
                res.push_back({nums[i], nums[l], nums[r]});
                while(l < r && nums[l] == nums[l + 1]) l++;
                while(l < r && nums[r] == nums[r - 1]) r--;

                l++; r--;
            }else if(sum < 0)
                l++;
            else
                r--;
        }
    }
    return res;
}

int main()
{
    vector<int> nums = {-1,0,1,2,-1,-4};
    vector<vector<int>> result = threeSum(nums);
    cout << "***TRIPLETS***\n";
    for(const auto& triplet : result){
        cout << '[';
        for(int i = 0; i < 3; ++i)
            cout << triplet[i] << (i < 3 - 1 ? ", " : "");
        cout << ']' << endl;
    }
    return 0;
}
