#ifndef _TEACHER_H_
#define _TEACHER_H_
#include<string>
#include"Student.h"
using namespace std;
class Teacher{
    private:
        string name;
        Student student;
    public:
        Teacher();
        Teacher(string name,Student student);
        void setStudent(Student student);
        Student getStudent();
        static void teachInfo();
        static int teacherCount;
};
#endif