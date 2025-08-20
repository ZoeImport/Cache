#include<iostream>
#include<string>
#include"struct.h"
using namespace std;
//struct&pointerVoid.h中函数定义
//此处使用地址传递，保证形参的修改得以对实参的值进行修改
void swap_byme(int *num_1,int *num_2){
  int temp;
  temp=*num_1;
  *num_1=*num_2;
  *num_2=temp;
}
/*
  如果不使用地址传递，使用值传递，就无法对实参进行修改，在对函数调用时就相当于将传入的值创建了一个新的副本
  对于以上的这种情况为了减少空间的浪费，就可以使用地址传递，但是对于地址传递来说，对传入的数据就有被修改的风险，此时就需要用到const关键字
  例如如下定义的函数showInfo()
*/

void showInfo(const Person *p){
  cout<<"Name:"<<p->name<<endl;
  cout<<"Age:"<<p->age<<endl;
  cout<<"Gender:"<<p->gender<<endl;
}

/*
  对于值传递来说，简单的sum函数为例
*/
int numSum(int num_1,int num_2){
  return num_1+num_2;
}

/*
  无参数传入，同时函数返回值为局部变量的引用类型
*/
int &showRef1(){
  int a=10;
  return a;
}
int & showRef2(){
  static int a=10;
  return a;
}

void constRef(const int& num){
  cout<<"num:"<<num<<endl;
}

//函数的默认参数
void defaultVoid(int num){
  cout<<"num:"<<num<<endl;
}


//函数的重载，其中函数的参数个数不同，种类不同

void overLoadVoid(){
  cout<<"this void is original"<<endl;
}

void overLoadVoid(int num){
  cout<<"this void is overload "<<endl;
}

void overloadFunc(int &num){
  cout<<"this void has not const"<<endl;
}
void overloadFunc(const int &num){
  cout<<"this void has const"<<endl;
}


