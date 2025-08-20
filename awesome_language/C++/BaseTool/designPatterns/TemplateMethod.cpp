#include <iostream>

// 抽象类：角色
class Character {
public:
  void attack() const {
    prepareWeapon();
    performAttack();
    cleanUp();
  }

  virtual void prepareWeapon() const = 0;
  virtual void performAttack() const = 0;
  virtual void cleanUp() const = 0;
};

// 具体类：战士
class Warrior : public Character {
public:
  void prepareWeapon() const override {
    std::cout << "Warrior is preparing sword." << std::endl;
  }

  void performAttack() const override {
    std::cout << "Warrior is slashing with sword." << std::endl;
  }

  void cleanUp() const override {
    std::cout << "Warrior is cleaning up." << std::endl;
  }
};

// 具体类：法师
class Mage : public Character {
public:
  void prepareWeapon() const override {
    std::cout << "Mage is preparing staff." << std::endl;
  }

  void performAttack() const override {
    std::cout << "Mage is casting fireball." << std::endl;
  }

  void cleanUp() const override {
    std::cout << "Mage is resting." << std::endl;
  }
};

int main() {
  Warrior warrior;
  Mage mage;

  warrior.attack();
  mage.attack();

  return 0;
}
