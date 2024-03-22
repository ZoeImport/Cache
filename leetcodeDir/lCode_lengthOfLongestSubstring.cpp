#include <algorithm>
#include <iostream>
#include <string>
#include <unordered_set>
#include<unordered_map>
using namespace std;
namespace lCode {
int lengthOfLongestSubstring1(string s) {
  unordered_set<char> char_set(s.size());
  int len = s.size();
  // creat right pointer for the last of window
  auto rp = -1;
  auto ans = 0;
  // use a range for left pointer
  for (auto lp = 0; lp < len; ++lp) {
    // erase the first of the window if  which is not the first of string
    if (lp != 0) {
      char_set.erase(s[lp - 1]);
    }
    //iterate for lp and judge (left pointer less than len and character in right pointer is not in car_set)
    while (lp +1< len && !char_set.count(s[rp + 1])) {
        //fit the condition so insert this character s[rp+1]
      char_set.insert(s[rp + 1]);
      //and make it left moving for left pointer
      ++rp;
    }
    //for every iterating for window to compute max length for subString
    ans = max(ans, rp - lp + 1);
  }
  return ans;
}
    auto lengthOfLongestSubstring2(string s){
        auto len =s.size();
        unordered_map<char,int>char_map(len);
        auto ans=0;
        auto lp=0;
        for (auto rp=0;rp<len;++rp) {
            if(char_map.count(s[rp])){
                lp=max(lp,char_map.at(s[rp])+1);
            }
            ans=max(ans,rp-lp+1);
            char_map[s[rp]]=rp;
        }
        return ans;

    }

} // namespace lCode


int main() {
    /*
    "abcabcbb"
    "bbbbb"
    "pwwkew"
    */
        string s = "pwwkew";
        cout << "lengthOfLongestSubstring : "
             << lCode::lengthOfLongestSubstring2(s) << endl;
        ;
}