#include <algorithm>
#include <iostream>
#include <iterator>
#include <map>
#include <memory>
#include <stack>
#include <string>
#include <utility>
#include <vector>

using namespace std;

namespace lCode {
    string reverseWords(string s) {
        auto begin=s.begin();
        auto str_end=s.begin();
        stack<string>wordsStack;
        string ans="";
        while (begin!=s.end()) {
            while ((*begin)==' ') {
                begin++;
            }
            str_end=begin;
            while ((*str_end)!=' '&&(str_end!=s.end())) {
                str_end++;
            }
            if (!string(begin,str_end).empty()) {
                wordsStack.push(string(begin,str_end));
                begin=str_end;
            }
        }
        while (!wordsStack.empty()){
            ans+=wordsStack.top();
            wordsStack.pop();
            ans+=!wordsStack.empty()?" ":"";
        }
    return ans;
    }
    string reverseWords2(string s){
        auto str_start=s.begin();
        auto str_end=str_start;
        // auto blank_start = str_start;
        // auto blank_end=str_start;
        // auto blank_count=0;
        reverse(s.begin(),s.end());
        while (str_start!=s.end()) {
            while ((*str_end) == ' ') {
                str_end++;
                // blank_count++;
            }
            
            
                // blank_end=str_end;
                // s.erase(str_start,str_end);
            
            // auto temp1=string(str_start,str_end);
            str_start=str_end;
            while ((*str_end!=' ')&&str_end!=s.end()) {
                str_end++;
            }
            // cout<<"*str_start:  "<<(*str_start)<<" *str_end:  "<<(*str_end)<<endl;
            auto temp2=string(str_start,str_end);
            reverse(str_start,str_end);
            
            str_start=str_end;
        }
        return s;
    }
}

int main(){
    string str1 = "hello world this is China";
    cout<<"\""<<lCode::reverseWords(str1)<<"\""<<endl;
    cout<<"=================================="<<endl;
    string str2 = "two good   example";
    string str3 = "two good                        example";
    cout<<"\""<<lCode::reverseWords2(str3)<<"\""<<endl;

    // string str3 = "abcdefg";
    // reverse(str2.begin(),str2.begin());
    // cout<<"\""<<str2<<"\""<<endl;
    // str2.erase(str3.begin()+1,str3.begin()+1);
    // cout<<"\""<<str3<<"\""<<endl;
    
    
    
    
}