#include <algorithm>
#include <iostream>
#include <vector>


using namespace std;

int maxArea(vector<int> &height) {
  int len = height.size();
  auto l = 0;
  auto r = len - 1;
  auto ans = 0;
  while (l < r) {
    auto area = min(height[l], height[r]) * (r - l);
    ans = max(ans, area);
    if (height[l] <= height[r]) {
      ++l;

    } else {
      --r;
    }
  }
  return ans;
}

int main() {
  vector<int> height{1, 8, 6, 2, 5, 4, 8, 3, 7};
  cout << maxArea(height);
}