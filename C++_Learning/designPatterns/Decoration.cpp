#include <iostream>

class Coffee {
public:
  virtual double cost() const = 0;
};

class Espresso : public Coffee {
public:
  double cost() const override { return 1.99; }
};

class Latte : public Coffee {
public:
  double cost() const override { return 2.49; }
};

class CoffeeDecorator : public Coffee {
protected:
  Coffee *coffee;

public:
  CoffeeDecorator(Coffee *c) : coffee(c) {}

  double cost() const override {
    if (coffee) {
      return coffee->cost();
    }
    return 0.0;
  }
};
class MilkDecorator : public CoffeeDecorator {
public:
  MilkDecorator(Coffee *c) : CoffeeDecorator(c) {}

  double cost() const override {
    if (coffee) {
      return coffee->cost() + 0.5; // 添加牛奶费用
    }
    return 0.0;
  }
};

class SugarDecorator : public CoffeeDecorator {
public:
  SugarDecorator(Coffee *c) : CoffeeDecorator(c) {}

  double cost() const override {
    if (coffee) {
      return coffee->cost() + 0.2; // 添加糖费用
    }
    return 0.0;
  }
};
int main() {
  Coffee *espresso = new Espresso();
  std::cout << "Espresso cost: $" << espresso->cost() << std::endl;

  Coffee *latte = new Latte();
  latte = new MilkDecorator(latte);  // 添加牛奶
  latte = new SugarDecorator(latte); // 再添加糖
  std::cout << "Latte cost: $" << latte->cost() << std::endl;
  return 0;
}

/*
  设计模式中的装饰模式旨在不破坏待装饰类中基础结构，在新增装饰器中增加原待装饰类能力
  基础装饰器为抽象类包含一个待装饰类对象成员变量
  装饰器实现类实现基础方法，对其进行拓展
*/