#ifndef _STRUCT_
#define _STRUCT_
#include<string>
using namespace std;
//使用标准命名空间的string
//struct
struct Person{
  string name;
  int age;
  char gender;
};

struct Student{
  string name;
  string lesson;
};

struct Teacher{
  string name;
  Student stu;
};
#endif