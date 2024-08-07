#include <iostream>
#include <vector>

class Command {

public:
  virtual void excute() = 0;
  virtual std::string name() const = 0;
};

class TurnOnTV : public Command {
public:
  void excute() override {
    std::cout << name() << std::endl;
    std::cout << "turn on TV over" << std::endl;
  }
  std::string name() const override { return "turnOn tv"; }
};

class TurnOffTV : public Command {
public:
  void excute() override {
    std::cout << name() << std::endl;
    std::cout << "turn off TV over" << std::endl;
  }
  std::string name() const override { return "turnOff tv"; }
};

class TurnOnWindow : public Command {
public:
  void excute() override {
    std::cout << name() << std::endl;
    std::cout << "turn on window over" << std::endl;
  }
  std::string name() const override { return "turnOn window"; }
};

class TurnOffWindow : public Command {
public:
  void excute() override {
    std::cout << name() << std::endl;
    std::cout << "turn off window over" << std::endl;
  }
  std::string name() const override { return "turnOff window"; }
};

class Remote {

private:
  std::vector<Command *> commands;

public:
  void addCommand(Command *command) { commands.push_back(command); }
  void excuteCommand(int index) {
    if (index >= 0 && index < commands.size()) {
      commands[index]->excute();
      return;
    } else {
      std::cout << "invalid index" << std::endl;
    }
  }
};

int main() {

  Remote *remot = new Remote;
  TurnOnTV *onTv = new TurnOnTV;
  TurnOffTV *offTv = new TurnOffTV;
  TurnOnWindow *onWin = new TurnOnWindow;
  TurnOffWindow *offWin = new TurnOffWindow;

  remot->addCommand(onTv);
  remot->addCommand(offTv);
  remot->addCommand(onWin);
  remot->addCommand(offWin);

  remot->excuteCommand(0);
  remot->excuteCommand(2);
  remot->excuteCommand(1);
  remot->excuteCommand(3);
}
