//谓词
//返回bool类型的仿函数

#include <type_traits>
#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;

class MyCompareOne{
    public:
        //一元谓词
        //返回第一个大于5的数
        bool operator()(int val){
            return val>5;
        }
};

class MyCompareTwo{
    public:
        //二元谓词
        //反转排序逻辑
        bool operator()(int valFirst,int valSecond){
            return valFirst>valSecond;
        }

};
int main(){
    vector<int> v1;
    v1.push_back(1);
    v1.push_back(3);
    v1.push_back(2);
    v1.push_back(9);
    v1.push_back(7);
    auto it=find_if(v1.begin(),v1.end(),MyCompareOne());
    if (it!=v1.end()) {
        cout<<*it<<endl;
    }

    sort(v1.begin(),v1.end(),MyCompareTwo());
    for (auto num :v1) {
        cout<<num<<" | ";
    }
}