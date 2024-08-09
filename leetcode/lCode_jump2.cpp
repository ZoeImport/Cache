#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

int jump(vector<int> &nums) {
  int len = nums.size();
  int maxIndex = 0;
  int steps = 0;
  auto end = 0;
  for (auto index = 0; index < len - 1; ++index) {
    maxIndex = max(maxIndex, index + nums[index]);
    if (index == end) {
      end = maxIndex;
      ++steps;
    }
  }
  return steps;
}

int main() {
  vector<int> nums{2, 3, 1, 1, 4};
  cout << jump(nums);
}