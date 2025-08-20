#include <iostream>
#include <string>

class Battery {
public:
  virtual std::string getBattery() = 0;
};

class CommonBattery : public Battery {
public:
  std::string getBattery() override { return "Common Battery"; }
};

class UltraBattery : public Battery {
public:
  std::string getBattery() override { return "Ultra Battery"; }
};

class Screen {
public:
  virtual std::string getScreen() = 0;
};

class CommonScreen : public Screen {
public:
  std::string getScreen() override { return "Common screen"; }
};

class UltraScreen : public Screen {
public:
  std::string getScreen() override { return "Ultra screen"; }
};

class Phone {
public:
  Phone(Battery *battery, Screen *screen) : battery(battery), screen(screen){};
  std::string getInfo() {
    return "Info:" + battery->getBattery() + ":" + screen->getScreen();
  }

private:
  Battery *battery = nullptr;
  Screen *screen = nullptr;
};

class PhoneFactory {
public:
  virtual Phone *createPhone() = 0;
};

class CommonFactory : public PhoneFactory {
  Phone *createPhone() override {
    Phone *phone = new Phone(new CommonBattery, new CommonScreen);
    std::cout << "Common phone created ";
    return phone;
  }
};

class UltraFactory : public PhoneFactory {
  Phone *createPhone() override {
    Phone *phone = new Phone(new UltraBattery, new UltraScreen);
    std::cout << "Ultra phone created ";
    return phone;
  }
};

int main() {
  PhoneFactory *phonefactory = new CommonFactory;
  Phone *phone = phonefactory->createPhone();
  std::cout << phone->getInfo();
}
