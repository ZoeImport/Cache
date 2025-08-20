#include<iostream>
#include<string>
#include"struct.h"
#include"struct&pointerViod.h"
using namespace std;

int main(){
  //结构体声明以及初始化
  Person p1={"tom",18,'M'};
  cout<<"name:"<<p1.name<<":age:"<<p1.age<<":gender"<<p1.gender<<endl;
  //创建结构体数组
  Person stu[3]={
    {"aaa",1,'M'},
    {"bbb",2,'M'},
    {"ccc",3,'W'}
  };
  for(int i=0;i<3;i++){
    cout<<"name:"<<stu[i].name<<"|age:"<<stu[i].age<<"|gender:"<<stu[i].gender<<endl;
  }
  //对于结构体对象的属性读写需要通过.操作符进行，即以上使用的stu[i].age以及p1.name等
  //但是对于结构体指针的属性读写则不同具体在指针后进行叙述
  cout<<"=============================================================================="<<endl;
  //pointer
  //指针的创建（int 类型为例）
  int num_1=10;
  int num_2=20;
  int *ptr1=&num_1;
  cout<<"p1:"<<ptr1<<endl;
  cout<<"sizeof(ptr1):"<<sizeof(ptr1)<<endl;
  cout<<"*p1:"<<*ptr1<<endl;
  /*
  输出结果：
  p1:0x7ffcf1f417fc
  sizeof(ptr1):8
  *p1:10
  */
  /*
    所以对于指针一个关键性的概念就是，指针是用于存放地址的变量
    两个重要的操作符：& *
    &：取址符
    *：解引用
  */

  //对于结构体指针属性的读写需要的操作符为->，例如下方的
  Person p2={"Jack",18,'M'};
  Person *ptr3=&p2;
  cout<<"name:"<<ptr3->name<<":age:"<<ptr3->age<<":gender"<<ptr3->gender<<endl;

  cout<<"====================================================================="<<endl;

  //值传递与地址传递
  //利用头文件中的swap_byme函数进行测试
  //地址传递
  int num_3=33;
  int num_4=44;
  swap_byme(&num_3,&num_4);
  cout<<"num_3:"<<num_3<<"|num_4:"<<num_4<<endl;
  //使用const关键字以确保地址传递在节省空间的同时不会修改原数据（需要时）
  showInfo(&p2);
  //值传递cout<<"ref2:"<<ref2<<endl;可以进行结构体的嵌套即一位老师可以包含一个或多个学生对象，此处只举单个的例子
  Teacher tech1={"Miss Li",{"Lucy","Ch"}};
  cout<<"teacher name:"<<tech1.name<<"  teacher's student's name and whose class is :"<<tech1.stu.name<<"|"<<tech1.stu.lesson<<endl;
  
  /*
    new关键字
    new关键字用于在堆开辟内存，需要使用delete关键字进行内存的释放
  */
  int *ptr4=new int(66);
  cout<<*ptr4<<endl;
  delete(ptr4);
  int *intArr=new int[5];
  for(int i=0;i<5;i++){
    intArr[i]=i;
  }
  for(int i=0;i<5;i++){
    cout<<intArr[i]<<endl;
  }
  delete[]intArr;
  for(int i=0;i<5;i++){
    cout<<intArr[i]<<endl;
  }

  cout<<"====================================================="<<endl;
  //引用
  /*
    引用的特性：
    1.引用一旦创建绑定不可以修改（指针常量）
    2.引用创建必须初始化
  */
  int num_6=66;
  int &ref1=num_6;
  cout<<"ref1:"<<ref1<<endl;
  /*
    引用在作为函数进行地址传递时，不需要像指针一样对参数进行取址符，而是直接进行参数通过引用传递
    函数不应该局部变量的引用
    函数的调用可以作为左值
  */
  // int &ref2=showRef1();
  // cout<<"ref2:"<<ref2<<endl;//第一行可以输出局部变量的值
  // cout<<"ref2:"<<ref2<<endl;//第二行因为变量内存的释放无正确值
  //此时如果对局部变量加上static关键字就可以使其在整个程序的结束才释放，保持其数据持久
  //函数的调用作为左值就代表修改了函数内部静态局部变量的值
  int &ref3=showRef2();
  cout<<"ref3:"<<ref3<<endl;
  cout<<"ref3:"<<ref3<<endl;
  showRef2()=22222;//此处对函数的左值进行赋值相当于对局部静态变量赋值
  cout<<"ref3:"<<ref3<<endl;
  cout<<"ref3:"<<ref3<<endl;

  //引用的本质
  //引用的本质是指针常量，即*const ，其指向是不可以更改的，并且一旦声明必须要进行初始化不可为null
  
  //常量引用const &
  //常量引用的原因：由于值传递需要创建一个新的副本，会增加内存的使用造成浪费，所以使用引用，防止内存的浪费，
  //但是由于引用会使得引用的变量存在不安全修改的可能，所以加上const关键字，使得其只可读不可写
  //换句话说常量引用就是常量指针常量(const int * const )，仅可读不可修改值与指向，这就是通过常量引用而不是值传递的原因
  int num_7=77;
  constRef(num_7);

  cout<<"========================================================================="<<endl;
  
  //函数拓展

  //函数的默认参数
  //函数的默认参数就是在函数的参数区域内直接进行默认参数设定，这样在函数调用时就算没有传入对应参数，也可以使用默认参数进行调用
  //要求:
  //1.函数的参数中某一个设定了默认参数，其后的所有参数也需要设定默认参数
  //2.函数的声明和实现中只能出现一个默认参数设定

  defaultVoid();
  defaultVoid(num_7);

  //函数的参数占位符，在参数列表中，可以只写变量类型而不写变量名（后续补充）
  //例如：  void add(int a,int);

  //函数的重载
  //函数重载需要的条件：
  //1.函数重载需要在同一个作用域内
  //2.函数同名与函数类型相同
  //3.函数参数需要拥有不同个数，不同种类
  
  overLoadVoid();
  overLoadVoid(num_7);

  //函数重载注意事项：
  //函数参数加上const代表只有可读属性，对于函数的重载来说加上const也可以实现函数的重载

  const int&num_8=10;
  overloadFunc(num_7);
  overloadFunc(num_8);
  // this void has not const
  // this void has const
  //说明函数重载时，对于参数const属性也会进行区别
  
}