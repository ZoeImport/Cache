#include <iostream>

class Communicate {
public:
  virtual void speak() = 0;
};

class Speaker : public Communicate {
public:
  void speak() override {
    std::cout << "speaker can speak by themselves" << std::endl;
  }
};

class Phone : Communicate {
public:
  Phone(Speaker *speaker) : speaker(speaker) { this->phoneOn = true; }

  bool getPhone() { return this->phoneOn; }

  void setPhone(bool phoneStatus) { this->phoneOn = phoneStatus; }
  void speak() override {
    if (this->getPhone()) {
      std::cout << "speaker can speak by phone" << std::endl;
    }
  }

private:
  bool phoneOn;
  Speaker *speaker;
};

int main() {
  Speaker *sp1 = new Speaker;
  sp1->speak();
  Phone *sp2 = new Phone(new Speaker);
  std::cout<<sp2->getPhone()<<std::endl;
  sp2->speak();
}