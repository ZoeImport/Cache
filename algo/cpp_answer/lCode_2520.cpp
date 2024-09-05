#include <charconv>
#include <iostream>
#include <iterator>
#include <string>
using namespace std;

namespace prob2520 {
    int countDigits1(int num){
        auto temp=num;
        auto count=0;
        while (temp) {
            if(num%(temp%10)==0)
            count+=1;
        temp=temp/10;
        }
        return count;
    }
    auto countDigits2(int num){
        auto str=to_string(num);
        auto count=0;
        for (auto ch :str) {
            if(num%(ch-'0')==0)++count;//ch->int
        }
        return count;
    }
}

int main(){
    cout<<prob2520::countDigits1(121)<<endl;
    cout<<prob2520::countDigits2(121)<<endl;
}

