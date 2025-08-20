#include<string>
#include<iostream>
#include"Student.h"
using namespace std;
Student::Student(){

}
Student::~Student(){
    // cout<<this->name<<" was killed"<<endl;
}
Student::Student(string name,int age,char gender){
    this->name=name;
    this->age=age;
    this->gender=gender;
}
void Student::setAge(int age){
    this->age=age;
}

int Student::getAge()const{
    return this->age;
}
void Student::setName(string name){
    this->name=name;
}
string Student::getName(){
    return this->name;
}
void Student::showAge() const{
    cout<<this->getAge()<<endl;
}

