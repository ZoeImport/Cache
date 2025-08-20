#ifndef BALL_H
#define BALL_H

#include <iostream>

class Ball{
    public:
        Ball() { std::cout << "Ball was created" << std::endl;}
        //纯虚析构函数的声明
        virtual ~Ball()=0;

};
//纯虚析构函数的定义
Ball::~Ball() { std::cout << "Ball was destroyed" << std::endl; }
class BasketBall:public Ball{
    public:
        BasketBall(){ std::cout<<"Basketball was created"<<std::endl;}
        virtual ~BasketBall() { 
            std::cout << "Basketball was destroyed" << std::endl;
         }
};
void ballLife() { 
    Ball *ball = new BasketBall; 
    delete ball;
}


#endif