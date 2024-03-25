#include <iostream>
#include <vector>

using namespace std;

vector<int> productExceptSelf(vector<int> &nums) {

  int len = nums.size();
  vector<int> left(len, 0);
  vector<int> right(len, 0);
  vector<int> ans(len);
  left[0] = 1;
  right[len - 1] = 1;
  for (auto index = 1; index < len; ++index) {
    left[index] = nums[index - 1] * left[index - 1];
  }
  for (auto index = len - 2; index >= 0; --index) {
    right[index] = nums[index + 1] * right[index + 1];
  }
  for (auto index = 0; index < len; ++index) {
    ans[index] = left[index] * right[index];
  }
  return ans;
}

int main() {
  vector<int> nums{1,2,3,4};
  auto res = productExceptSelf(nums);
  for (auto &num : res) {
    cout << num << " ";
  }
}