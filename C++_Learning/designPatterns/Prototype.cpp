#include <iostream>

class Person {
public:
  virtual Person *clone() = 0;
  virtual void whoami() = 0;
};

class Person_001 : public Person {
public:
  Person *clone() override { return new Person_001(*this); }
  void whoami() override { std::cout << "this is person 001" << std::endl; }
};

class Person_002 : public Person {
public:
  Person *clone() override { return new Person_002(*this); }
  void whoami() override { std::cout << "this is person 002" << std::endl; }
};

// 原型模式
int main() {

  //通过父类指针克隆子类对象
  Person *person = new Person_001;
  Person *p1 = person->clone();
  p1->whoami();

  person = new Person_002;
  Person *p2 = person->clone();
  p2->whoami();
}