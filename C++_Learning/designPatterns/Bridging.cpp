#include <iostream>
#include <map>
#include <string>

class Person {
public:
public:
  Person(std::string name, std::string job, int sallary)
      : name(name), job(job), sallary(sallary){};
  std::string getName() { return this->name; }
  std::string getJob() { return this->job; }

private:
  std::string name;
  std::string job;
  int sallary;
};

class Team {
public:
  // Team(std::string name) : name(name){};
  void addMember(Person *person) { teamInfos[person->getName()] = person; }

  void showInfos() {
    std::cout << "team name :" << this->name << std::endl;
    for (auto &info : this->teamInfos) {
      std::cout << info.first << ":" << info.second->getJob() << std::endl;
    }
  }
  virtual void aims() = 0;

private:
  std::string name;
  std::map<std::string, Person *> teamInfos;
};

class Ship {
public:
  Ship(Team *team) : team(team){};
  void showTeam() {
    this->team->showInfos();
    this->team->aims();
  }
  virtual void flags() = 0;

private:
  Team *team = nullptr;
};

class MainTeam : public Team {
public:
  using Team::Team;
  void aims() override { std::cout << "Teams' aims is Main..." << std::endl; }
};

class MainShip : public Ship {
public:
  using Ship::Ship;
  void flags() override { std::cout << "flags is Main..." << std::endl; }
};

int main() {
  Team *mainTeam = new MainTeam;
  Person *p1 = new Person("aaa", "job1", 111);
  Person *p2 = new Person("bbb", "job2", 222);
  Person *p3 = new Person("ccc", "job3", 333);
  mainTeam->addMember(p1);
  mainTeam->addMember(p2);
  mainTeam->addMember(p3);
  MainShip *Ship = new MainShip(mainTeam);
  Ship->showTeam();
  Ship->flags();
}