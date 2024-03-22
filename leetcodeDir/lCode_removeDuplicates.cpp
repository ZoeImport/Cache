// #include <algorithm>
#include <iostream>
#include <set>
#include <vector>
using namespace std;

namespace lCode {
int removeDuplicates(vector<int> &nums) {
  set<int> ans;
  for (auto &num : nums) {
    if (ans.count(num) == 0) {
      ans.insert(num);
    }
  }
  auto index=0;
  for (auto &num :ans) {
    nums[index++]=num;
  }
  return ans.size();
}
} // namespace lCode

int main() {
  vector<int> nums = {0,0,1,1,1,2,2,3,3,4};
  lCode::removeDuplicates(nums);
  for (auto num : nums) {
    cout << num << " ";
  }
}