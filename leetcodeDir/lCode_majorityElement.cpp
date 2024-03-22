#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int majorityElement(vector<int> &nums) {
  
  auto len=nums.size();
  if (len==1) {
    return nums[0];
  }
  auto slow=0;
  auto fast=1;
  auto count =1;
  auto major=len/2;
  sort(nums.begin(),nums.end());
  while (fast<len) {
    if(nums[slow]==nums[fast]){
      ++fast;
      ++count;
      if(count>major)return nums[slow];
    }else {
      count=1;
      fast++;
      slow=fast;
    }
  }
  return -1;
}

int main() {

  vector<int> nums{2, 2, 1, 1, 1, 2, 2};
  cout << majorityElement(nums);
}