#ifndef PERSON_H
#define PERSON_H

#include <iostream>


class Person{
    public:
        Person()=default;
        virtual void work()const{
            std::cout<<"Person is  working"<<std::endl;            
        }
};
class Son:public Person{
    public:
        Son()=default;
        void work()const{
            std::cout<<"Son is working"<<std::endl;
        }
};
class Daughter:public Person{
    public:
        Daughter()=default;
        void work()const{
            std::cout<<"Daughter is  working"<<std::endl;
        }
};
void doWork(const Person &person){
    person.work();
}


#endif