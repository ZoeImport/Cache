//set
/*
    set之中不允许出现重复元素，multiset可以出现重复元素
 插入元素：

    insert(val): 插入值为val的元素到set中，如果值已经存在，将会被忽略。

2. 删除元素：

    erase(val): 删除值为val的元素。
    erase(iterator): 通过迭代器删除指定元素。
    erase(first, last): 删除指定范围内的元素。

3. 查找元素：

    find(val):
查找值为val的元素，返回指向该元素的迭代器，如果找不到，则返回end()。 count(val):
返回值为val的元素的数量（0或1，因为set中元素唯一）。

4. 迭代器：

    begin(): 返回指向第一个元素的迭代器。
    end(): 返回指向尾部的迭代器。

5. 其他查询操作：

    empty(): 检查set是否为空。
    size(): 返回set中元素的数量。
    clear(): 清空set中的所有元素。

6. 获取有序范围：

    lower_bound(val): 返回一个指向不小于val的第一个元素的迭代器。
    upper_bound(val): 返回一个指向大于val的第一个元素的迭代器。
    equal_range(val): 返回一个pair，包含了lower_bound和upper_bound的迭代器。

7. 比较操作：

    == 和 != 操作符：用于比较两个set是否相等。
    <, <=, >, >= 操作符：用于比较两个set的大小关系。

8. 自定义排序规则：
您可以通过提供自定义的比较函数或函数对象来定义set的排序规则。例如，在创建set时，可以传递比较函数作为第二个参数。

cpp

std::set<int, MyComparator> myCustomSet;

9. 复制和合并set：

    swap(otherSet): 交换两个set的内容，将otherSet的内容复制到当前set中。
    insert(otherSet.begin(), otherSet.end()): 将另一个set的元素插入到当前set中。
    
*/

#include <set>
#include <iostream>
using namespace std;

int main(){
    set<int> intSet;
    multiset<int>multiSet;
    
    //数据不可重复
    intSet.insert(2);
    intSet.insert(2);
    intSet.insert(1);
    intSet.insert(3);
    intSet.insert(4);
    intSet.insert(5);
    
    //数据可重复且自动排序
    multiSet.insert(2);
    multiSet.insert(3);
    multiSet.insert(1);
    multiSet.insert(2);
    multiSet.insert(5);
    multiSet.insert(4);
    
    for (int num : intSet) {
        cout<<num<<" ";
    }
    cout<<endl;
    for (int num :multiSet) {
        cout<<num<<" ";
    }
}