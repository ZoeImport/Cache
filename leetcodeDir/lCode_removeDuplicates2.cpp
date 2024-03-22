#include <iostream>
#include <vector>
// #include <algorithm>

using namespace std;

int removeDuplicates(vector<int>& nums) {
  auto len=nums.size();
  if (len<=2) {
    return len;
  }
  auto fast=2;
  auto slow=2;
  while (fast<len) {
    if(nums[slow-2]!=nums[fast]){
      nums[slow]=nums[fast];
      ++slow;
    }
    ++fast;
  } 
  return slow;
}

int main(){
  vector<int> nums{1,1,1,2,2,3};
  cout<<removeDuplicates(nums);
  for (auto num :nums) {
    cout<<num<<" ";
  }

}