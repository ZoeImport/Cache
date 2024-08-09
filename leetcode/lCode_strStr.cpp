#include <iostream>
#include <string>
#include <vector>

using namespace std;

int strStr(string haystack, string needle) {
  int len_m = haystack.length();
  int len_p = needle.length();
  if (!len_p) {
    return 0;
  }
  vector<int> next(len_p, 0);
  auto l = 0;

  for (auto r = 1; r < len_p; ++r) {
    while (l > 0 && needle[l] != needle[r]) {
      l = next[l - 1];
    }
    if (needle[l] == needle[r]) {
      ++l;
    }
    next[r] = l;
  }

  for (auto m = 0, n = 0; m < len_m; ++m) {
    while (n > 0 && haystack[m] != needle[n]) {
      n = next[n - 1];
    }
    if (haystack[m] == needle[n]) {
      ++n;
    }
    if (n == len_p) {
      return m - len_p + 1;
    }
  }
  return -1;
}

int main() {
  string m = "asadbutsad";
  string n = "sad";
  cout << strStr(m, n);
}