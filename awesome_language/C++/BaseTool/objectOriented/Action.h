#ifndef ACTION_H
#define  ACTION_H
#include <iostream>

class Action{
    public:
        //此处声明work为虚函数，同时该类只有虚函数,所以该类为抽象类
        virtual void work()=0;
};
class Swam:public Action{
    public:
        void work() override{
            std::cout<<"Swaming"<<std::endl;
        }
};




#endif