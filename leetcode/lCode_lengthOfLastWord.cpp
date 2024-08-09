#include <cctype>
#include <iostream>
#include <string>

using namespace std;

int lengthOfLastWord(string s) { 
  auto ans=0;
  int len = s.size();
  if (len==1) {
    return 1;
  }
  for (auto index = len - 1;index>=0 ;--index) {
    if (isalpha(s[index])) {
      ++ans;
    }else if (ans){
      break;
    }
  }
  return ans;
}


int main() {
  string s="s ";
  cout<<lengthOfLastWord(s);
  
}