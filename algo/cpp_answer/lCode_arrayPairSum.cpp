#include <algorithm>
#include <utility>
#include <vector>
#include <iostream>

using namespace std;

namespace lCode {   
    auto arrayPairSum(vector<int>& nums){
        auto sum=0;
        sort(nums.begin(),nums.end());
        auto start=0;
        for (auto i=0;i<nums.size()/2;i++) {
            sum+=nums[start];
            start+=2;
        }
        return sum;;   
    }
}

int main(){
    vector<int>nums={6,2,6,5,1,2};
    cout<<lCode::arrayPairSum(nums);
}