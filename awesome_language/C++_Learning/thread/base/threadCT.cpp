#include <algorithm>
#include <functional>
#include <iostream>
#include <mutex>
#include <thread>
#include <string>
#include "Thread_guard.h"//RAII
//thread
using namespace std;
//construct
void myPrint(const  string &msg){
    cout<<"msg: "<<msg<<endl;
}
void printInt(int &num){
    cout<<"num: "<<num<<endl;
}


//mutex 锁（互斥体）
//当一个锁被一个线程所持有并且锁定时，进入临界区，在此期间的其他试图访问临界区的线程都会被阻塞，知道目前临界区的锁释放
mutex mtx;
static int num=0;
void sumNumber(){
    for (int index=0;index<10000;++index) {
        mtx.lock();
        num++;
        mtx.unlock();
    }
}

class Functor{
    public:
        void operator()(int num){
            cout<<"functor print num: "<< num<<endl;
        }
};

class Func{
    public:
        void myPrint(int num){
            cout<<"no static func print num: "<<num<<endl;
        }
        static void printInt(int num){
            cout<<"static func print num: "<<num<<endl;
        }
};

int main(){
    //线程构造方法
    int num1=999;
    //1.function
    thread threadPrint1(myPrint,"hello world");
    //2.Lambda
    thread threadPrint2([num1](){
        cout<<"this is a lambda function"<<endl;
        cout<<num1<<endl;
    });
    //3.functor
    thread threadPrint4(Functor(),333);
    threadPrint4.join();
    //4.no_static_member_function
    Func f;
    //非静态成员变量属于单个对象需要利用对象进行绑定
    thread threadPrint5(&Func::myPrint,f,55);
    threadPrint5.join();
    //5.static_member_func
    thread threadPrint6(&Func::printInt,66);
    threadPrint6.join();
    
    //join:主线程会等待调用join的线程执行完毕后再销毁
    //detach:将调用该方法的线程分离,主线程不会再等待该线程

    //PS：注意若线程被detach分离后就是以并发的方式进行，如果该线程对当前局部作用域的变量有使用，那么就有可能在局部变量被销毁后出现意想不到的效果
    //所以在使用detach分离线程时，尽可能做到值传递，除非可以保证传入的局部变量的引用和指针不会在线程结束之前被销毁
    //无论是调用join()还是detach()之前都应该检查线程是否是joinable的双重的join或者detach都会使得程序终止
    
    if (threadPrint1.joinable()) {
        threadPrint1.join();
    }
    threadPrint2.join();

    int num2=20;
    //对于其构造函数，默认会将传入的参数拷贝到线程空间，即使传递的是引用，如果需要线程更新传递引用的对象就需要使用std::ref
    thread threadPrint3(printInt,ref(num2));
    threadPrint3.join();

    thread sumThread1(sumNumber);
    thread sumThread2(sumNumber);
    cout << "sumThread1: " << sumThread1.get_id() << endl;
    sumThread1.join();
    sumThread2.join();
    cout<<num<<endl;

    //线程是不可复制的但可以移动(movable)

    //获取线程的ID
    //通过线程调用get_id()
    //在当前线程调用this_thread::get_id()

    cout<<"main thread: "<<this_thread::get_id()<<endl;
    cout << "sumThread1: " << sumThread1.get_id() << endl;

    //放弃当前线程使得系统选择另一线程继续执行
    //yield()

    //sleep_until(sleep point)   sleep_for(time span)
    //to be continued...

    
} 