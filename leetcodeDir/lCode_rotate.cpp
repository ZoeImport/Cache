#include <iostream>
#include <vector>

using namespace std;

void rotate(vector<int> &nums, int k) {
  int n = nums.size();
  vector<int> cache = nums;
  for (int i = 0; i < n; ++i) {
    nums[(i + k) % n] = cache[i];
  }
}

int main() {
  vector<int> nums{1, 2, 3, 4, 5, 6, 7};
  rotate(nums, 3);
  for (auto x : nums) {
    cout << x << " ";
  }
}