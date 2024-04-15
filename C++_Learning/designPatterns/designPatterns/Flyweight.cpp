#include <iostream>
#include <map>
#include <memory>
#include <string>

class Monster {
private:
  std::string name;
  int health;
  int attack;
  static int kinds;

public:
  Monster(std::string name, int health, int attack)
      : name(name), health(health), attack(attack) {
    std::cout << "Kinds of monsters is" << (kinds++) << std::endl;
  };
  void display() {
    std::cout << "Monster info:" << name << ":" << health << ":" << attack
              << std::endl;
    std::cout << "Monster address:" << this << std::endl;
  }
};
int Monster::kinds = 0;

class MonsterFactory {
private:
  std::map<std::string, std::shared_ptr<Monster *>> monsterMap;

public:
  std::shared_ptr<Monster *> getMonster(const std::string &name, int health,
                                        int attack) {
    std::string key =
        name + ":" + std::to_string(health) + ":" + std::to_string(attack);
    if (this->monsterMap.find(key) == this->monsterMap.end()) {
      // not exist
      this->monsterMap[key] =
          std::make_shared<Monster *>(new Monster(name, health, attack));
    }
    return this->monsterMap[key];
  }
};

int main() {
  MonsterFactory *mf = new MonsterFactory;
  auto m1 = mf->getMonster("Kick", 100, 5);
  auto m2 = mf->getMonster("Kick", 100, 5);
  auto m3 = mf->getMonster("Bomb", 20, 99);

  (*m1)->display();
  (*m2)->display();
  (*m3)->display();
/*
           Kinds of monsters is0
           Kinds of monsters is1
           Monster info:Kick:100:5
           Monster address:0x5617b2d1aef0
           Monster info:Kick:100:5
           Monster address:0x5617b2d1aef0
           Monster info:Bomb:20:99
           Monster address:0x5617b2d1b3b0
*/
}