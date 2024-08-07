#ifndef _STU_CLASS_
#define _STU_CLASS_
#include<string>
// using namespace std;

class Student{
    private:
        std:: string name;
        mutable int age;
        char gender;
    public:
        Student();//空参构造
        Student(std::string name,int age,char gender);
        ~Student();
        void setAge(int age);
        int getAge()const;
        void setName(std::string name);
        std::string getName();
        void showAge() const;
};

#endif