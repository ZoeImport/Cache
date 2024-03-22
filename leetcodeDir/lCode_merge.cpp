#include <algorithm>
#include <vector>
#include <iostream>
using namespace std;

namespace lCode {
void merge(vector<int> &nums1, int m, vector<int> &nums2, int n) {
  int ptr_1 = m - 1;
  int ptr_2 = n - 1;
  int cur = m + n - 1;
  while (ptr_1 >= 0 && ptr_2 >= 0) {
    nums1[cur--] =
        nums1[ptr_1] > nums2[ptr_2] ? nums1[ptr_1--] : nums2[ptr_2--];
  }
  while (ptr_1 >= 0) {
    nums1[cur--] = nums1[ptr_1--];
  }
  while (ptr_2 >= 0) {
    nums1[cur--] = nums2[ptr_2--];
  }
}
} // namespace lCode
int main(){
  cout<<"ok";
}