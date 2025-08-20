//STL（standard template library）
/*
STL（Standard Template
Library）是C++标准库的一部分，提供了一组通用的模板类和函数，用于实现常见的数据结构和算法。
STL的目标是为C++程序员提供高效的、可复用的工具，以减少开发时间、提高代码质量和性能。
STL包括几个关键组件，其中最重要的包括容器、算法和迭代器。
以下是STL的主要组件：

    容器（Containers）：
    STL提供了多种容器类型，如向量（vector）、链表（list）、双向链表（deque）、栈（stack）、队列（queue）、优先队列（priority_queue）、映射（map）、集合（set）等
    算法（Algorithms）：STL包括一系列通用算法，如排序、查找、遍历、变换等。这些算法可以应用于各种容器类型，使其成为可复用的工具。一些常见的算法包括sort、find、for_each、transform等。
    迭代器（Iterators）：迭代器是STL中非常重要的概念。它们是用于遍历容器中元素的通用接口。STL提供了多种迭代器类型，包括输入迭代器、输出迭代器、正向迭代器、双向迭代器和随机访问迭代器。迭代器允许你在不暴露底层数据结构的情况下遍历容器中的元素。
    函数对象（Functors）：STL允许你定义函数对象，也称为谓词（predicates），它们是可调用对象，通常用于算法的自定义行为。函数对象可以以类似函数的方式使用，例如，用于比较、排序和筛选容器中的元素。
    适配器（Adapters）：STL还提供了适配器，用于将一个容器适应成另一个容器类型。例如，stack和queue都是基于deque的适配器，用于实现栈和队列。
    智能指针（SmartPointers）：C++11引入了智能指针，如shared_ptr和unique_ptr，它们是STL的一部分，用于管理动态分配的内存，以避免内存泄漏和提高程序的安全性。
    其他组件：STL还包括其他一些组件，如字符串处理（string类）、日期时间处理、输入输出流操作符重载等。
    PS：上述介绍摘自ChatGPT3.5
*/

//vector容器
#include <vector>
#include <iostream>
using namespace std;

int main(){
    vector<int>v1;
    //添加
    v1.push_back(1);
    v1.push_back(6);
    v1.push_back(2);
    v1.push_back(4);
    v1.push_back(5);

    cout<<v1.at(2)<<endl;
    //使用迭代器遍历
    vector<int>::iterator it1=v1.begin();
    while (it1!=v1.end()) {
        cout<<*it1<<endl;
        it1++;
    }
    //C++11增强for
    for(int num:v1){
        cout<<num<<",";
    }
    /*
        构造和初始化：
        std::vector<T> v;：创建一个空的 vector 对象。
        std::vector<T> v(size);：创建一个包含 size 个默认初始化值的 vector。
        std::vector<T> v(size, value);：创建一个包含 size 个值为 value 的vector。 
        std::vector<T> v(otherVector);：创建一个包含另一个 vector 的副本的vector。 
        std::vector<T> v(begin, end);：创建一个包含范围 [begin, end) 的vector。

    元素访问：
        v[index]：访问指定索引位置的元素。
        v.at(index)：安全地访问指定索引位置的元素，会抛出异常如果索引越界。
        v.front()：访问第一个元素。
        v.back()：访问最后一个元素。
        v.data()：获取指向vector数据的指针。

    容量：
        v.size()：返回 vector 中的元素数量。
        v.empty()：检查 vector 是否为空。
        v.capacity()：返回当前分配的内存容量。
        v.reserve(newCapacity)：为 vector 分配至少 newCapacity 大小的内存。

    修改容器：
        v.push_back(value)：将元素添加到 vector 的末尾。
        v.pop_back()：删除 vector 的末尾元素。
        v.insert(iterator, value)：在指定位置插入一个元素。
        v.erase(iterator)：删除指定位置的元素。
        v.clear()：清空 vector 中的所有元素。

    遍历：
        使用范围循环（Range-based for loop）或迭代器来遍历 vector 中的元素。

    查找和排序：
        v.find(value)：查找特定值的元素，需要在头文件 <algorithm> 中使用。
        std::sort(v.begin(), v.end())：对 vector 中的元素进行排序，需要在头文件
    <algorithm> 中使用。

    其他操作：
        v.swap(otherVector)：交换两个 vector 的内容。
        v.resize(newSize)：改变 vector 的大小。
        v.shrink_to_fit()：减小 vector 的容量以匹配当前元素数量。
    */

    /*
    std::vector 的扩容规则通常是：

    倍增策略：std::vector 通常以倍增的方式来分配内存。
    当 std::vector需要扩容以容纳更多元素时，它会分配一个新的内存块，通常是当前容量的两倍，并将元素从旧内存块复制到新内存块。
    这个操作是为了减少频繁的内存分配和复制操作，提高性能。

    递增策略：有时，std::vector
    可能会使用递增的策略，而不是严格的倍增。这意味着容量的增加可能会以某种常数（如4、8或16）递增。

    最小容量：std::vector
    在创建时通常有一小块初始容量，例如，通常情况下初始容量为0，但可以根据具体实现而有所不同。随着添加元素，容量会根据上述规则逐渐增加。

    分摊成本：由于扩容操作的成本是分摊到多次插入操作中的，因此在平均情况下，
    std::vector的插入操作具有常数时间复杂度。
    */
}
