#include <iostream>
#include <iterator>
#include <string>
using namespace std;


void catInfo(){
    cout<<"this is catInfo"<<endl;
}
//func Template
namespace voidTemplate {
    template <class T> T max(T a, T b) { return a > b ? a : b; }
}

//class Template
namespace classTemplate {
    template <class nameType,class ageType=int>
    class Person{
        public:
            nameType name;
            ageType age;
            Person()=default;
            Person(nameType name,ageType age):name(name),age(age){};
            void showInfo(){
                std::cout<<this->name<<","<<this->age<<std::endl;
            }
    };
    //在继承时需要指明实例的类型
    class Student:public Person<string,int>{
        public:
            int StudentId;
            public:
                Student()=default;
                // Student(string name,int age,int StudentId){
                //     this->name=name;
                //     this->age=age;
                //     this->StudentId=StudentId;
                // };
                Student(string name,int age,int StudentId):Person<string, int>(name,age),StudentId(StudentId){};
                //对于基类是模板类需要对基类的模板在初始化列表中指定
    
    };
    //如果希望子类不直接指定类型继承，就需要将子类也变为类模板
    template<class TeacherIdType,class PersonTYpe>
    class Teacher:public Person<PersonTYpe>{
        public:
            TeacherIdType TeacherId;
            Teacher()=default;
            Teacher(PersonTYpe person,TeacherIdType TeacherId):Person<PersonTYpe>(person),TeacherId(TeacherId){};
    };
    
    //对于构造函数和成员函数的类外实现需要加上模板参数
    template<class xType,class yType>
    class Point{
        public:
            xType x;
            yType y;
            Point()=default;
            Point(xType x,yType y);
            void showInfo();
    };
    //类外实现Point类的有参构造和成员方法
    template <class xType, class yType>
    Point<xType,yType>::Point(xType x, yType y):x(x),y(y){}
    template<class xType,class yType>
    void Point<xType,yType>::showInfo(){
       cout<<this->x<<","<<this->y<<endl;
    }
}
namespace friendVoid {
    template <class sizeType>
    class Ball{
        //全局函数做友元的类内实现
        friend void showInfo(){
            cout<<"this is showInfo"<<endl;
        }

        //全局函数的类外实现
        friend void catInfo();
        public:
            sizeType size;
            Ball()=default;
            Ball(sizeType size):size(size){};
            
    };
}

int main(){
// template
// 函数模板和普通函数调用顺序：
// 如果普通函数和函数模板都可以实现，调用普通函数
// 可以使用空模板参数强制调用函数模板
// 函数模板可以发生重载
// 如果模板可以实现更好的匹配就调用函数模板
    cout << voidTemplate::max(1, 3) << endl;

//类模板可以自动进行类型推导
    classTemplate::Person("Lucy",18).showInfo();
    classTemplate::Person(18,18).showInfo();
//类模板可以在类型中有默认参数
    classTemplate::Person<std::string>("Tom",18).showInfo();

//类模板中的成员函数只有在被调用时才被创建
//普通类中的成员函数在一开始就创建


//类模板对象做函数参数
//1.指定传入的类型
//2.参数模板化
//3.整个类模板化

//类模板的继承
//子类进行类模板的继承时，子类在声明时，需要指定父类模板参数的类型
//如果想要灵活指定父类模板类型，就需要让子类也变成模板类

    classTemplate::Point<int, int>(20,20).showInfo();

    //全局函数做类模板的友元
    //全局函数在类内实现：直接在类内声明友元
    //全局函数在类外实现：需要让编译器提前知道全局函数的存在






    //namespace命名空间
    /*
    1. 命名空间的定义
        命名空间通过关键字namespace来定义，后面跟着命名空间的名称，通常以大写字母开头
    2. 命名空间的作用

    命名空间主要有两个作用：
            解决命名冲突：当不同的库或代码库使用相同的名称时，会导致命名冲突。通过将它们放入不同的命名空间，你可以避免这种冲突。
        这有助于将不同库中的相同名称的函数、变量或类进行隔离，以允许它们在相同的程序中共存。
        提高代码的可读性和可维护性：命名空间可以将相关的变量、函数和类分组在一起，使代码更具结构性。这使得代码更易于理解、维护和扩展。
    3. 命名空间的使用
            在C++中，你可以使用命名空间中的成员，方法是在成员名称前面加上命名空间的名称，使用作用域解析运算符::
    4. 命名空间的嵌套
            C++允许嵌套命名空间，这意味着你可以在一个命名空间内再定义另一个命名空间
    5. 匿名命名空间
            C++中还有一个特殊的匿名命名空间，用于定义仅在当前文件中可见的内容。它可以防止其他文件中的命名冲突。
例如：
namespace {
    int localVar; // 仅在当前文件中可见
}

    6. 使用命名空间的注意事项
    避免滥用命名空间，不要将所有内容都放在全局命名空间中。
    命名空间的名称应该具有描述性，以便代码的可读性。
    在头文件中，尽量避免在全局命名空间中定义内容，以减少命名冲突的风险。
    不要在头文件中打开命名空间，应该将命名空间的定义限制在源文件中。


    using关键字：
    1.类型别名：using MyInt=int;
    2.命名空间别名：using namespaceClass=namespace1::namespace2;
    3.模板别名：using MyVector=std::vector<T>;
    4.函数指针别名：using MyFunctionPointer = void(*)(int);

    */
}