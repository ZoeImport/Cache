#include <iostream>
#include <numeric>
#include <vector>
#include <algorithm>

using namespace std;

namespace lCode {
    auto findMaxConsecutiveOnes(vector<int> &nums)->int{
        auto maxCount=0;
        auto olderCount=0;
        nums.resize(nums.size()+1);
        
        nums[nums.size()-1]=0;
        for (auto index=0;index<nums.size();++index) {   
            while (nums[index]) {
                cout << "count:" << maxCount <<"|"<< "index:" << index<<endl;
                ++maxCount;
                ++index;
            }

            olderCount=maxCount>olderCount?maxCount:olderCount;
            maxCount=0;
        }
        return olderCount;
    }
}

int main(){
    vector<int>nums{1,0,1,1,1};
    // auto nums2=vector<int>(6,0);
    cout<<lCode::findMaxConsecutiveOnes(nums)<<endl;
    // cout<<lCode::findMaxConsecutiveOnes(nums2)<<endl;
}