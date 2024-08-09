#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

int hIndex(vector<int> &citations) {
  sort(citations.begin(), citations.end());
  auto ans = 0;
  int index = citations.size() - 1;
  while (index >= 0 && citations[index] > ans) {
    ++ans;
    --index;
  }
  return ans;
}

int main() {
  vector<int> nums{1,3,1};
  cout << hIndex(nums);
}