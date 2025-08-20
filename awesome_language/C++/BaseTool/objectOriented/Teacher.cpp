#include<string>
#include<iostream>
#include"Teacher.h"
using namespace std;
Teacher::Teacher(){

}
//此处构造方法的写法为初始化列表，通过  属性值(值),属性值(值),属性值(值) 进行创建对象
Teacher::Teacher(string name,Student student):name(name),student(Student(student)){}
void Teacher::setStudent(Student student){
    this->student.setName(student.getName());
}
Student Teacher::getStudent(){
    return this->student;
}
void Teacher::teachInfo(){
    cout<<"count of teachers is  "<<Teacher::teacherCount<<endl;
}
int Teacher::teacherCount=20;