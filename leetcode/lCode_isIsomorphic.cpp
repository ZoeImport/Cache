#include <iostream>
#include <string>
#include <unordered_map>
using namespace std;

bool isIsomorphic(string s, string t) {
  unordered_map<char, char> s2t;
  unordered_map<char, char> t2s;
  int len = s.length();
  for (int i = 0; i < len; ++i) {
    char x = s[i], y = t[i];
    if ((s2t.count(x) && s2t[x] != y) || (t2s.count(y) && t2s[y] != x)) {
      return false;
    }
    s2t[x] = y;
    t2s[y] = x;
  }
  return true;
}

bool isIsomorphic2(string s, string t) {

  int len_s = s.size();
  int len_t = t.size();
  if (len_s != len_t) {
    return false;
  }
  unordered_map<char, char> mp;
  for (auto index = 0; index < len_s; ++index) {
    if (mp.find(s[index]) == mp.end() && mp.find(t[index]) == mp.end()) {
      // if not contain
      mp[s[index]] = t[index];
      mp[t[index]] = s[index];
      for (auto x : mp) {
        cout << x.first << ":" << x.second << endl;
      }
      cout << index << "==========" << endl;
    } else if (mp[s[index]] != t[index]) {
      return false;
    }
  }
  return true;
}

int main() { cout << isIsomorphic(string("paper"), string("title")) << endl; }