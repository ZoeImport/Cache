#include <iostream>
#include <mutex>
#include <thread>
static int count=0;
void add(){
    for (auto index=0;index<100000;++index) {
        ++count;
    }
}
//mutex
std::mutex mt;

//lock_guard
//简化互斥量的使用，减少手动释放锁可能带来的问题
static int sum=0;
void addLock(){
    for (auto index =0;index<100000;++index) {
        //创建lock_guard对象(需要传入mutex对象)
        //在作用域结束时对象自动解锁互斥量
        std::lock_guard<std::mutex>lg(mt);
        ++sum;
    }
}

//unique_lock

int main(){
    std::thread add_common_1(add);
    
    std::thread add_common_2(add);
    add_common_1.join();
    add_common_2.join();
}