//pair对组
#include <iostream>
#include <string>
#include <utility>
using namespace std;
int main(){
    //第一种创建方式直接创建
    pair<int, string> pair1(1,"Lucy");
    pair<int, string> pair2(2,"Tom");
    //第二种利用make_pair()
    pair<int,string> pair3=make_pair(3,"Bob");
    // int tempInt;
    // string tempStr;
    pair1.swap(pair2);
    cout<<(pair1==pair2)<<endl;
    cout<<pair1.first<<":"<<pair1.second<<endl;
    auto [tempInt,tempStr] = pair1;
    cout<<tempInt<<" | "<<tempStr<<endl;
    
    
}