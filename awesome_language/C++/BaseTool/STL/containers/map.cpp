//map
/*
insert 函数： 用于将键值对插入到 std::map 中。

emplace 函数： 用于以更高效的方式插入元素，支持在一个函数调用中构造键值对。

[] 操作符： 用于访问和修改 std::map 中的元素。

find 函数： 用于查找指定键的元素，返回一个迭代器。

erase 函数： 用于删除指定键的元素。

clear 函数： 用于清空整个 std::map。

size 函数： 用于获取 std::map 中元素的数量。

empty 函数： 用于检查 std::map 是否为空。

begin 和 end 函数： 用于获取迭代器，可用于遍历 std::map 中的元素。

count 函数： 用于计算特定键的元素在 std::map
中的个数（通常为0或1，因为键是唯一的）。

*/

#include <map>
#include <iostream>
#include <string>
#include <utility>
using namespace std;

int main(){
    map<int,string>map1;
    
    //构造pair插入
    map1.insert(make_pair(2, "Lucy"));
    map1.insert(make_pair(1, "Tom"));
    map1.insert(make_pair(4, "Bob"));
    map1.insert(make_pair(3, "David"));
    //利用emplace
    map1.emplace(6,"111111111");
    
    map1.erase(2);

    for (auto num :map1) {
        cout<<num.first<<" | "<<num.second<<endl;
    }

    cout<<map1.count(1)<<endl;
    

}