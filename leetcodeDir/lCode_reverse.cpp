#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

int reverse(int x){
  string s=to_string(x);
        std::reverse(s.begin(), s.end());
        int ans=0;
        try{
            ans=stoi(s);
            if (x<0) ans=-ans;
        }catch(exception ex){}
        return ans;
}

int main(){
  cout<<reverse(321)<<endl;
}