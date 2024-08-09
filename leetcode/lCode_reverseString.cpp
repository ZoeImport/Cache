#include <any>
#include <iostream>
#include <vector>

using namespace std;

namespace lCode {
    auto reverseString(vector<char> &s){
        auto start=0;
        auto tail =s.size()-1;
        while (start<tail) {
            swap(s[start++],s[tail--]);
        }
    }
}

int main(){
        auto s = vector<char>{
            'h', 'e', 'l', 'l', 'o', 'w', 'o','r','l','d'
        };
        // cout<<*s.end();
        lCode::reverseString(s);
        for (auto ch :s) {
            cout<<ch<<" ";
        }
}