#include <string>

using namespace std;

string longestPalindrome(string s){
  int len=s.length(),maxLen=1;
  string ans="";
  for (auto index=0;index<(2*len-1); ++index) {
    auto l=index/2,r=l+(index%2);
    while (l>=0&&r<len&&s[l]==s[r]) {
      if((r-l+1)>maxLen){
        maxLen=l-r+1;
        ans=s.substr(l,maxLen-1);
      }
      --l,++r;
    }
  }
  return ans;
}
int main(){
  
}