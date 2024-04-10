#include <iostream>

class Animal {
public:
  virtual void action() = 0;
  // virtual ~Animal()=0;
};

class Cat : public Animal {
  void action() override { std::cout << "cat miao miao miao" << std::endl; }
};

class Dog : public Animal {
  void action() override { std::cout << "dog wang wang wang" << std::endl; }
};

class Pig : public Animal {
  void action() override { std::cout << "pig heng heng heng" << std::endl; }
};

enum class Type : char { DOG, CAT, PIG };
class AnimalFactory {
public:
  Animal *create(Type type) {
    Animal *ptr = nullptr;
    switch (type) {
    case Type::DOG: {
      ptr = new Dog;
      break;
    }
    case Type::CAT: {
      ptr = new Cat;
      break;
    }
    case Type::PIG: {
      ptr = new Pig;
      break;
    }
    }
    return ptr;
  }
};

int main() {
  AnimalFactory *factory = new AnimalFactory;
  // Polymorphism
  Animal *animal = factory->create(Type::DOG);
  animal->action();
}