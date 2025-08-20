#ifndef _POINT_H
#define _POINT_H
#include<iostream>
class Point{
    public:
        int x;
        int y;
        Point();
        Point(int x,int y);
        //运算符重载声明
        //<<
        friend std::ostream& operator<<(std::ostream &out,const Point &point);
        //++
        //前置++
        Point& operator ++(int);
        //后置++
        Point operator++();
        //--
        //前置--
        Point& operator--(int);
        //后置--
        Point operator--();
        //== !=
        bool operator==(Point &point);
        bool operator!=(Point &point);
        //=
        Point& operator=(Point &point);
        //()
        void operator()(Point &point);
        

};

#endif