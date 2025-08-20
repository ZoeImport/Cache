#ifndef _ANIMAL_H
#define _ANIMAL_H

#include<iostream>


class Animal{
    public:
    int Size;
         void speak()const {
            std::cout<<"animal speak"<<std::endl;
        }
};
//公有继承
class Cat:virtual public Animal{
    public:
    // int Size;
        void speak()const{
            std::cout<<"cat speak"<<std::endl;
        }
        
        
};
class Dog:virtual public Animal{
    public:
    // int Size;
        void speak()const{
            std::cout<<"dog speak"<<std::endl;
        }
};
class DogCat:public Cat,public Dog{
    public:
        // int Size;
         void speak(){
            std::cout<<"dogCat speak"<<std::endl;
        }
};








#endif