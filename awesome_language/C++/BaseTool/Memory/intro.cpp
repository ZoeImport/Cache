#include <iostream>
#include <memory>
#include <utility>

using namespace std;

//use shared from this to self
class A:public enable_shared_from_this<A>{
    auto get_self(){
        return shared_from_this();
    }
};
class B:public enable_shared_from_this<B>{
    public:
    B(){
      cout<<" B ct is over"<<endl;  
    }
    ~B(){
        cout<<" B dt is over"<<endl;
    }
    void setSelf(){
        m_share=shared_from_this();
    }
    private:
        shared_ptr<B> m_share;
};
int main(){
    // smart pointer
    //unique_pointer
    /*
    unique_pointer has not copyCt and assignmentCt,which only can be moved
    unique_ptr(const unique_ptr&) = delete;
    unique_ptr& operator=(const unique_ptr&) = delete;
    */
    // ct
    unique_ptr<int>up1=make_unique<int>(10);
    //make unique do not need new because its sourceCode has already implement that
    cout<<" up1 : "<<up1.get()<<" *up1 : "<<*up1<<endl;
    unique_ptr<int>up2(new int(20));

    unique_ptr<int>up3;
    up3.reset(new int(30));

    unique_ptr<int []>up4(new int[10]);
    //It's not be permitted to use * operator for unique(T[]),and only can use [] operator to get it
    cout<<" up4 : "<<up4.get()<<endl;
    for (auto index=0;index<10;++index) {
        up4[index]=index;
    }
    //get() be used to get source object address(so it's a pointer of source obj)
    cout << " up4.get() : " << up4.get()<<" *up4.get() : " <<*up4.get()<< endl;
    //move a unique pointer
    unique_ptr<int>up5;
    up5=move(up1);
    cout<<" up5 : "<<up5.get()<<endl;
    cout<<" up1 : "<<up1.get()<<endl;

    //shared_pointer
    /*
    shared pointer can be copy and assignment to a newly shared pointer 
    */
    //shared pointer can make it that multiple pointer can point a same obj and also can use use_count() to get the count about
    //how many pointer has pointed that obj
    shared_ptr<int>sp1(new int(10));
    cout<<" sp1 : "<<sp1<<" *sp1 : "<<*sp1<<endl;
    shared_ptr<int>sp2(sp1);
    cout<<" sp2 : "<<sp2<<" *sp2 : "<<*sp2<<endl;
    cout<<" the use count : "<<sp1.use_count()<<endl;
    /*
    sp1 : 0x56430f1a9750 *sp1 : 10
    sp2 : 0x56430f1a9750 *sp2 : 10
    the use count : 2
    */
    shared_ptr<int>sp3=make_shared<int>(20);
    // enable_shared_from_this can be used to return a current obj(this)
    /*
    智能指针最初设计的目的就是为了管理堆对象的（即那些不会自动释放的资源）
    一个资源的生命周期可以交给一个智能指针对象，但是该智能指针的生命周期不可以再交给整个资源来管理
    陷阱一：不应该共享栈对象的 this 给智能指针对象
    陷阱二：避免 std::enable_shared_from_this 的循环引用问题
    */
    {
        shared_ptr<B>sp_b(new B());
        sp_b->setSelf(); // B ct is over but not have dt happen
    }
    
    //weak_pointer
    shared_ptr<int> sp4(new int(20));
    cout<<" use count of sp4 : "<<sp4.use_count()<<endl;
    weak_ptr<int> wp1(sp4);
    cout<<" use count of sp4's obj : "<<sp4.use_count()<<endl;
    //so wek pointer will not add the count of referencing source obj  
    auto wp2=wp1.lock();//lock can return a shared pointer
    //weak pointer can use expired to check whether it has source referencing
    {
        shared_ptr<int> sp5(new int(50));
        weak_ptr<int>wp3(sp5);
        if(wp3.expired()) cout << " source is expired ";
        else cout<<" not expired ";
    }

    //last the size of smart pointer 
    //32bit :up 4               sp wp:8 
    //64bit :up 8               sp wp:16
}