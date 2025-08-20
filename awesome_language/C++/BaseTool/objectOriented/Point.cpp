#include<iostream>
#include"Point.h"
Point::Point(){}
Point::Point(int x,int y):x(x),y(y){}
std::ostream& operator<<(std::ostream &cout , const Point &point){
    std::cout<<"("<<point.x<<","<<point.y<<")"<<std::endl;
    return cout;
}
Point Point::operator++(){
    Point temp(*this);
    this->x++;
    this->y++;
    return temp; 
}
Point& Point::operator++(int){
    this->x++;
    this->y++;
    return *this;
}
Point Point::operator--(){
    Point *temp;
    temp->x=this->x;
    temp->y=this->y;
    this->x--;
    this->y--;
    return *temp; 
}
Point& Point::operator--(int){
    this->x--;
    this->y--;
    return *this;
}
bool Point::operator==(Point &point){
    return(this->x==point.x&&this->y==point.y);
}
bool Point::operator!=(Point &point){
    return!(*this==point);
}
Point& Point::operator=(Point &point){
    this->x=point.x;
    this->y=point.y;
    return *this;
}
void Point::operator()(Point &point){
    std::cout<<point<<std::endl;
}
