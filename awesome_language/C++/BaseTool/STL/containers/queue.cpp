//queue
/*
创建和初始化：

    std::queue<T> myQueue;：创建一个空的队列。
    std::queue<T> myQueue(container)：使用另一个容器 container 来初始化队列，将
container 的元素复制到队列中。

入队列和出队列：

    myQueue.push(value)：将元素 value 入队列。
    myQueue.pop()：将队列前端的元素出队列。

队列前端元素：

    myQueue.front()：返回队列前端的元素，但不删除它。

队列大小和空检查：

    myQueue.size()：返回队列中的元素数量。
    myQueue.empty()：检查队列是否为空
*/
#include <iostream>
#include <queue>
#include <algorithm>

using namespace std;

int main(){
    queue<int>que;
    que.push(1);
    que.push(2);
    que.push(3);
    que.push(3);
    //队列的提供的接口受限所以没有直接的for范围遍历
    //通过利用pop() front()将元素依次出队遍历或者拷贝到一个新的容器中
    while (!que.empty()) {
        cout<<que.front()<<" ";
        que.pop();
    }
}