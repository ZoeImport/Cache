#include<iostream>
#include<string>
#include"Student.h"
#include"Teacher.h"
#include"Point.h"
#include"Animal.h"
#include "Person.h"
#include "Ball.h"
using namespace std;
//面向对象篇
//面向对象特性：封装
//三个权限关键词：private protected public
//private:  类内可以直接使用，类外不可直接使用
//protected:类内可以直接使用，类外不可直接使用，子类可以使用
//public:   类内可以直接使用，类外可以直接使用


//this指针：成员函数和成员变量是分开存储的，对于每一个成员函数在C++中只会创建一份实例，为了区分同一类型的不同对象的调用就需要this指针
//即this指针指向被调用成员函数所属的对象
//this指针用途：
//1.在形参与成员变量同名时，就可以用this指针进行区分
//2.在类的非静态成员函数中返回对象本身return *this


//构造函数，    析构函数，构造拷贝函数
//构造函数：    创建对象（默认空定义）
//析构函数：    释放对象（默认空定义）
//构造拷贝函数： 对象进行拷贝时调用的函数，默认为值传递
//如果重写了构造函数和析构函数，构造拷贝函数可以不写（保持值传递），如果重写了构造拷贝函数就需要重写构造函数和析构函数

//深拷贝与浅拷贝
//浅拷贝：将存储的东西进行复制
//深拷贝：在堆内存中重新开辟一块新的空间再进行复制


int main(){
    //创建Student对象
    //调用构造方法的三种方式:
    //括号法：
    //Ps：在使用括号法调用时，调用无参构造不需要使用空的小括号即不该写为Student stu();因为编译器会认为这句话是声明一个函数，应该写为Student stu;
    Student stu1;//无参构造
    Student stu2("Tom",18,'M');

    //显示法：
    Student stu3=Student();
    Student stu4=Student("Lucy",20,'W');
    Student stu5=Student(stu2);//此处调用了构造拷贝函数（值传递）

    //创建匿名对象，匿名对象会在创建后被删除
    Student();//上方的显示法创建就是创建一个匿名对象再将对象传给stu3 stu4 stu5
    
    //隐式转换法：
    Student stu6={"Jack",22,'M'};
    
    // cout<<"name:"<<stu6.name<<" age:"<<stu6.age<<" gender:"<<stu6.gender<<endl;
    cout<<"Jack's age is "<<stu6.getAge()<<endl;
    
    /*
    程序输出：
         was killed
        Jack's age is 22
        Jack was killed
        Tom was killed
        Lucy was killed
        was killed
        Tom was killed
        was killed
    */


    //以上是对于Student对象的创建的一些概念
    //接下来创建Teacher对象，使用初始化列表进行构造函数定义
    
    //静态成员变量和静态成员函数
    //静态成员变量
    //1.所有成员共享一份变量
    //2.类内声明，类外初始化
    //3.在编译阶段分配内存

    //静态成员函数
    //1.所有对象共享一个函数
    //2.静态成员函数只能访问静态成员变量
    //Ps:原因：静态成员函数属于类，所有的对象共享一个成员函数，对于普通成员函数在创建时会为其创建一个this指针，使得其可以通过该指针区分调用它的对象
    //但是对于静态成员函数，并没有创建属于它的this指针，也就不能区分调用他的对象，从而也就不能在静态成员函数内部使用非静态成员变量
    
    Student stu7=Student("Tom",17,'M');
    Teacher teach1=Teacher("Lily",stu7);
    cout<<teach1.getStudent().getName()<<endl;
    
    //调用静态变量
    cout<<Teacher::teacherCount<<endl;
    //使用类名对静态成员方法进行调用，在函数中仅调用了静态成员变量
    Teacher::teachInfo();
    

    //常成员函数
    //常成员函数就是在funcName()后加上const,例如Student.h中的声明,普通成员函数相当于创建了一个指针常量(指向不能变)
    //在常成员函数中相当于加入const在this前加入const,即变成了常量指针常量(指向与值都不可变)
    //存在例外的是，假如一个成员属性被mutable修饰，那么它也可以更改
    
    stu7.showAge();
    
    //常对象
    //常对象只能调用常成员函数，因为常对象的属性值不可变
    //对于被mutable修饰的成员属性，也可以存在被修改的情况
    const Student stu8=Student("Lisa",22,'W');
    stu8.showAge();

    cout<<"===================================================="<<endl;
    //友元
    //使用友元的目的：让一个函数或者类访问另一个类的私有变量
    //友元的三种实现
    //1.全局函数做友元
    //2.类做友元
    //3.成员函数做友元
    
    //运算符重载
    //创建类Point对运算符<< ()++ ++() ()-- --() == !=  = () 几种运算符进行重载
    Point p1=Point(3,3);
    cout<<++p1<<endl;
    cout<<++p1<<endl;
    cout<<p1<<endl;
    Point p2;
    p2=p1;
    cout<<p2<<endl;
    cout<<(p1==p2)<<endl;
    p2++;
    cout<<(p1!=p2)<<endl;
    p1(p2);
    /*
    输出结果：
        (3,3)

        (4,4)

        (5,5)

        (5,5)

        1
        1
        (6,6)
    */
    cout<<"================================================"<<endl;
    
    //面向对象特性：继承
    //创建基类Animal,子类Cat Dog
    //三种继承中:公有public继承对权限原样保留,保护继承protected会将公有和保护属性继承为protected，私有继承private会将public,protected继承为private
    
    //对于继承中的同名函数和同名变量可以利用作用域进行区分
    //通过子类访问父类同名成员需要加作用域
    Cat().speak();
    Cat().Animal::speak();
    //对于菱形继承问题：解决方法为在继承基类时增加virtual关键字，在创建对象时就会把基类子类所有属性值设置为同一个
    //菱形问题：当基类存在一个变量并且出现菱形继承的多个子类以及子类的子类没有属于自己同基类的成员变量时，就会出现多个类对于一个变量拥有不同的值
    

    DogCat dogCat;
    // dogCat.Animal::Size=3;
    dogCat.Dog::Size=2;
    dogCat.Cat::Size=1;
    
    // cout<<dogCat.Animal::Size<<endl;
    cout<<dogCat.Dog::Size<<endl;//1
    cout<<dogCat.Cat::Size<<endl;//1
    cout<<dogCat.Size<<endl;     //1


    //面向对象特性：多态
    //多态满足条件：
    //1.有继承关系
    //2.子类重写父类中的虚函数


    //静态联编：对于doWork函数，假如在编译阶段函数的地址就确定就是静态联编
    /*
    静态联编（Static Binding）：
        也称为早期绑定或编译时绑定。
        在编译阶段确定要调用的函数或方法。编译器根据变量的静态类型（在编译时可知）来解析函数调用。
        静态联编通常用于非多态的情况，例如普通的函数调用或非虚函数的方法调用。
    */
    //动态联编：如果在运行阶段才能确定就是动态联编
    /*
    动态联编（Dynamic Binding）：

        也称为晚期绑定或运行时绑定。
        在运行时根据对象的实际类型来确定要调用的函数或方法。这通常与多态性相关，特别是在基类和派生类之间的虚函数调用中。
        动态联编允许在运行时适应不同的子类对象，使得程序更加灵活和多态。
    */

    //面对无论传入的是Person Son  Daughter都只会调用Person类的work方法，想要依据传入的对象类型进行不同的调用，就要使用virtual关键字实现多态
    doWork(Son()); // 若不在Person类中work函数加上virtual关键字 此处输出Person is  working
    // Son is working
    
    //纯虚函数与抽象类
    //纯虚函数声明: virtual void FuncName()=0;
    //对于纯虚函数需要在继承该类的子类中重写此函数
    //假如一个类中有纯虚函数就称这个类为抽象类(abstract),抽象类无法实例化对象

    //例如Action.h中定义与实现
    

    //虚析构和纯虚析构
    //相同点:
    //1.可以用来解决父类指针释放子类对象的问题
    //2.两种都需要具体函数实现
    //不同点：
    //如果是纯虚析构函数，就属于抽象类无法实例化，如果是虚析构就可以实例化

    ballLife();
    /*
    Ball was created
    Basketball was created
    Basketball was destroyed
    Ball was destroyed
    */
    
}