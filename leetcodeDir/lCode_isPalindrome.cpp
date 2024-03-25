#include <algorithm>
#include <cctype>
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

using namespace std;
bool isPalindrome(string s) {
  if (s.length() <= 1) {
    return true;
  }
  string str = "";
  for (auto &ch : s) {
    if (isalnum(ch)) {
      str += tolower(ch);
    }
  }
  string str_rev = string(str.rbegin(), str.rend());
  if (str_rev == str) {
    return true;
  }
  return false;
}

int main() {
  string str = "A man, a plan, a canal: Panama";
  cout << isPalindrome(str);
}