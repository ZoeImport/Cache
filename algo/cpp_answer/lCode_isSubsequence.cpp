#include <iostream>
#include <string>

using namespace std;

bool isSubsequence(string s, string t) {
  if (s.empty()) {
    return true;
  }
  int len_s=s.length();
  int len_t = t.length();
  auto ptr_s=0;
  
  for (auto ptr_t = 0;ptr_t<len_t;++ptr_t) {
    if (s[ptr_s]==t[ptr_t]) {
      ++ptr_s;
    }
    if(ptr_s==len_s)return true;
  }
  return false;
}

int main() {
  string s = "abc";
  string t = "ahbgdc";
  cout << isSubsequence(s, t);
}