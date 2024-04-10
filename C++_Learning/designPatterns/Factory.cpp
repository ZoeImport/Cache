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

class AnimalFactory {
public:
  virtual Animal *createAnimal() = 0;
};

class CatFactory : public AnimalFactory {
public:
  // Polymorphism
  Animal *createAnimal() override { return new Cat; }
};

class DogFactory : public AnimalFactory {
public:
  // Polymorphism
  Animal *createAnimal() override { return new Dog; }
};

class PigFactory : public AnimalFactory {
public:
  // Polymorphism
  Animal *createAnimal() override { return new Pig; }
};

int main() {
  AnimalFactory *animalfactory = new PigFactory;
  Animal *animal = animalfactory->createAnimal();
  animal->action();
}