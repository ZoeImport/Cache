#include <iostream>
#include <string>

class Foreigner {
public:
  virtual std::string say() = 0;
  void recv(std::string msg) { std::cout << msg << std::endl; }
};

class American : public Foreigner {
public:
  std::string say() override { return "Hello from USA"; }
};

class French : public Foreigner {
public:
  std::string say() override { return "Hello from France"; }
};

class Chinese {
public:
  void recv(std::string msg) { std::cout << msg << std::endl; }
  std::string send() { return "hello from China"; }
};

class Translater {
public:
  Translater(Foreigner *foreigner) : foreigner(foreigner){};
  virtual void transToPerson() = 0;
  virtual void transToForeign() = 0;

protected:
  Chinese person;
  Foreigner *foreigner = nullptr;
};

class TranslaterEn : public Translater {
public:
  using Translater::Translater;
  void transToPerson() override {
    std::string msg = foreigner->say();
    person.recv("USA say :" + msg);
  }
  void transToForeign() override {
    std::string msg = person.send();
    foreigner->recv(msg);
  }
};

class TranslaterFr : public Translater {
public:
  using Translater::Translater;
  void transToPerson() override {
    std::string msg = foreigner->say();
    person.recv("Frence say :" + msg);
  }
  void transToForeign() override {
    std::string msg = person.send();
    foreigner->recv(msg);
  }
};

int main() {
  Foreigner *f1 = new American;
  TranslaterEn *entransCN = new TranslaterEn(f1);
  entransCN->transToPerson();
  entransCN->transToForeign();
}