//list
/*
创建和初始化：

    std::list<T> myList;：创建一个空链表。
    std::list<T> myList(size, value);：创建一个包含 size 个值为 value的元素的链表。 
    std::list<T>myList(otherList);：创建一个包含另一个链表的副本的链表。 
    std::list<T>myList(first, last);：创建一个包含范围 [first, last) 的链表。

插入和删除元素：

    myList.push_back(value)：在链表末尾添加元素。
    myList.push_front(value)：在链表前端添加元素。
    myList.insert(iterator, value)：在指定位置插入元素。
    myList.pop_back()：删除链表末尾的元素。
    myList.pop_front()：删除链表前端的元素。
    myList.erase(iterator)：删除指定位置的元素。

访问元素：

    myList.front()：访问链表的第一个元素。
    myList.back()：访问链表的最后一个元素。

大小和空检查：

    myList.size()：返回链表中的元素数量。
    myList.empty()：检查链表是否为空。

遍历链表：

    使用迭代器进行遍历

    使用范围 for 循环来遍历链表中的元素。

其他操作：

    myList.clear()：清空链表中的所有元素。
    myList.splice(pos, otherList)：将另一个链表 otherList
的元素移动到当前链表的指定位置 pos。
*/

#include <iostream>
#include <list>
#include <algorithm>
using namespace std;

int main(){
    list<int>l1;
    l1.push_front(1);
    l1.push_front(3);
    l1.push_front(4);
    l1.push_front(8);
    l1.push_front(1);
    l1.push_front(9);
    l1.push_front(3);
    cout<<l1.back()<<endl;
    list<int>::iterator it=l1.begin();
    l1.erase(it);
    l1.reverse();
    for (int num :l1) {
        cout<<num<<" ";
    }
    
    
    
    
}