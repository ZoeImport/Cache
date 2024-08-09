#include <iostream>
#include <string>
#include <unordered_map>

using namespace std;

class Solution {
public:
  int romanToInt(string s) {
    auto ans = 0;
    int len = s.length();
    for (auto index = 0; index < len; ++index) {
      auto val = map[s[index]];
      if (index < len - 1 && map[s[index + 1]] > val) {
        ans -= val;
      } else {
        ans += val;
      }
    }
    return ans;
  }

private:
  unordered_map<char, int> map{
      {'I', 1},   {'V', 5},   {'X', 10},   {'L', 50},
      {'C', 100}, {'D', 500}, {'M', 1000},
  };
};

int main() {
  auto str = string("III");
  cout<<Solution().romanToInt(str);
}