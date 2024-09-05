#include <vector>
#include <iostream>

using namespace std;

namespace lCode {
    auto removeElement(vector<int> &nums,int val)->int{
        auto fast=0;
        auto slow=0;
        for(;fast<nums.size();++fast) {
            if (nums[fast]!=val) {
                nums[slow++]=nums[fast];
            }
        }
        return slow;
    }   
}

int main(){
    auto nums=vector<int>{1,2,3,4,2,2,2,2};
    auto len=lCode::removeElement(nums,2);
    cout<<len<<",";
    cout<<"[";
    for (auto index=0;index<len;++index) {
        cout<<nums[index];
        index==len-1?cout<<"":cout<<",";
    }  
    cout<<"]";
}