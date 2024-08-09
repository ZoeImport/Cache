#include <algorithm>
#include <cstddef>
#include <string>
#include <unordered_map>
#include <variant>
#include <vector>
#include <iostream>
using namespace std;

namespace lCode {
    auto longestCommonPrefix(vector<string> &strs){
        auto minLengthStr=strs[0];
        for (auto index=0;index<strs.size();index++) {
            if(strs[index].empty()){
                return string();
            }
            if(strs[index].length()<minLengthStr.length()){
                minLengthStr=strs[index];
            }
        }
        string prefix="";
        for (auto index:minLengthStr) {
            prefix+=index;
            for (auto str :strs) {
                if (str.find(prefix)!=0) {
                    prefix.pop_back();
                    return prefix;
                }    
            }
        }   
        
        return prefix ;
    }
}

int main() {
        vector<string> strs = {"flower", "flower", "flower", "flower"};
        cout << lCode::longestCommonPrefix(strs) << endl;
}