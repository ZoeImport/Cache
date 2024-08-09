#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

bool canJump(vector<int> &nums) {
  int len = nums.size();
  auto tail=0;
  for (auto index=0;index<len;++index) {
    if (index<=tail) {
      tail=max(tail,index+nums[index]);
      if(tail>=len-1)return true;
    }
  }
  return false;
}

int main() { cout << "ok"; }