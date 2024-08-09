#include <iostream>
#include <vector>

using namespace std;

namespace lCode {
    int pivotIndex(vector<int> &nums) {
        auto sum=0;
        auto sum_current=0;
        for (auto &num :nums) {
            sum+=num;
        }
        for (int i=0;i<nums.size();++i) {
            if(!(sum_current-((sum-nums.at(i))/2.0))){
                return i;
            }
            sum_current+=nums.at(i);
        }
        return -1;
    }

    int binSearch(vector<int> &nums, int target){
        auto min=0;
        auto max=nums.size()-1;
        while (min<=max) {
            auto mid=min+(max-min)/2;
            if(nums[mid]==target) return mid;
            else if (nums[mid]<target)min=mid+1;
            else max=mid-1;
        }
        return min;
    }

    
}
int main(){
    vector<int> vt;
    vt.push_back(1);
    vt.push_back(1);
    cout<<lCode::pivotIndex(vt)<<endl;
}