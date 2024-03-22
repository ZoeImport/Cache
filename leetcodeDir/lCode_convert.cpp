#include <iostream>
#include <string>
#include <vector>

using namespace std;

namespace lCode {
    string convert(string s, int numRows) {
        if(numRows==1)return s;
        string ans;
        int len=s.length();
        if (numRows>len) return s;
        vector<string> mat(numRows);
        auto index=0,flag=1;
        for (auto i=0;i<len;++i) {
          mat[index].push_back(s[i]);
          index+=flag;
          if(index==numRows-1||index==0)flag=-flag;
        }
        for (auto &str : mat) {
          ans+=str;
        }
        return ans;
    }
}

int main() { 
    string s = "PAYPALISHIRING";
    /*
    
    P     I    N
    A   L S  I G
    Y A   H R
    P     I
    
    */
    int numRows=4;
    cout<<"string s after converting : "<<lCode::convert(s,numRows)<<endl;

}