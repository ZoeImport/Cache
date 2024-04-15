#include <iostream>
#include <ostream>

class SubSystemA {
public:
  void preparationA() {
    std::cout<<"subsystem A is ready to run"<<std::endl;
  }
};


class SubSystemB {
public:
  void preparationB() {
    std::cout<<"subsystem B is ready to run"<<std::endl;
  }
};

class Appearance {
public:
  Appearance() {
    this->a = new SubSystemA;
    this->b=new SubSystemB;
  }
  void action() {
    this->a->preparationA();
    this->b->preparationB();
    std::cout<<"All is ready to run"<<std::endl;
  }
private:
  SubSystemA *a;
  SubSystemB *b;
};

int main() {
  Appearance *app = new Appearance;
  app->action();
}