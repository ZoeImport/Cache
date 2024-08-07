/*
    deque(双端队列)
    创建和初始化：

    std::deque<T>myDeque;：创建一个空的双端队列。
    std::deque<T>myDeque(size, value);：创建一个包含 size 个值为 value的元素的双端队列。 
    std::deque<T>myDeque(otherDeque);：创建一个包含另一个双端队列的副本的双端队列。 
    std::deque<T>myDeque(first, last);：创建一个包含范围 [first, last) 的双端队列。

元素访问：

    myDeque[i]：通过索引访问元素，与数组类似。
    myDeque.at(i)：安全地通过索引访问元素，会抛出异常如果索引越界。
    myDeque.front()：访问队列的第一个元素。
    myDeque.back()：访问队列的最后一个元素。

插入和删除元素：

    myDeque.push_back(value)：在队列的末尾添加元素。
    myDeque.push_front(value)：在队列的前端添加元素。
    myDeque.pop_back()：删除队列的末尾元素。
    myDeque.pop_front()：删除队列的前端元素。

容量相关函数：

    myDeque.size()：返回队列中的元素数量。
    myDeque.empty()：检查队列是否为空。
    myDeque.resize(newSize)：改变队列的大小。

迭代和遍历：

    for (const auto& element : myDeque)：使用范围循环来遍历双端队列。
    使用迭代器进行遍历，类似于其他STL容器。

其他操作：

    myDeque.clear()：清空队列中的所有元素。
    myDeque.swap(otherDeque)：交换两个双端队列的内容

*/
#include <iostream>
#include <deque>
#include <algorithm>
using namespace std;


int main(){
    deque<int> dq;
    dq.push_back(1);
    dq.push_back(2);
    dq.push_back(3);
    for (int num : dq) {
        cout<<num<<" ";
    }
    cout<<endl<<"============================="<<endl;
    dq.push_front(3);
    dq.push_front(3);
    dq.push_front(3);
    dq.push_front(3);
    for (int num : dq) {
        cout<<num<<" ";
    }
}