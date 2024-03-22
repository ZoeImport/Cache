#include <iostream>
#include <string>


// letcode 647
int countSubstrings(std::string s){
  int len=s.length(),ans=0;
  for (auto index=0;index<(2*len-1); ++index) {
    int l=index/2,r=l+(index %2);
    while (l>=0&&r<len&&s[l]==s[r]) {
      --l,++r,ans++;
    }
  }
    return ans;
}

int main(){
  std::string s="abc";
  std::cout<<countSubstrings(s)<<std::endl;
}