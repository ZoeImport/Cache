//stack
/*
    创建和初始化：
        std::stack<T> myStack;：创建一个空的栈。
        std::stack<T> myStack(container)：使用另一个容器 container
   来初始化栈，将 container 的元素复制到栈中。

    入栈和出栈：
        myStack.push(value)：将元素 value 入栈。
        myStack.pop()：将栈顶的元素出栈。

    栈顶元素：
        myStack.top()：返回栈顶的元素，但不删除它。

    容量相关函数：
        myStack.size()：返回栈中的元素数量。
        myStack.empty()：检查栈是否为空。

*/

#include <iostream>
#include <stack>
#include <vector>
using namespace std;

int main(){
    stack<int> st1;
    st1.push(1);
    st1.push(2);
    st1.push(3);
    st1.push(4);
    //对于栈来说，它并不提供范围遍历，所以想要遍历它
    //1.直接利用pop方法不断的弹出元素，缺点是改变原有数据
    //2.创建一个新的容器对stack的元素进行接收，再对新容器元素进行范围遍历
    vector<int >v1(st1.size());
    for (int size=0;size<v1.size(); ++size) {
        v1[size]=st1.top();
        st1.pop();
    }
    for (int num :v1) {
        cout<<num<<" ";
    }
    
}