#include <iostream>
#include <string>
#include <vector>

class Memo {
public:
  Memo()=default;
  Memo(std::string state):state(state){};
  std::string getState() { return this->state; }
  void setState(std::string state) {
    this->state=state;
  }
private:
  std::string state;
};

class Sponsor {
public:
  Sponsor() = default;
  std::string getState() { return this->state; }
  void setState(std::string state) { this->state = state; }
  Memo saveAsMemo() { return Memo(this->state); }
  void getFromMemo(Memo memo) { this->state = memo.getState(); }
  
private:
  std::string state;
};

class Manager {
public:
  Manager()=default;
  void addMemo(Memo memo) { memoArr.emplace_back(memo); }
  auto getMemo(int index) {
    if (index>memoArr.size()||index<0) {
      return Memo("valid index message");
    }
    return memoArr[index];
  }
  std::vector<Memo> memoArr;
  private:
};

int main() {
  Sponsor sponsr;
  Manager manager;
  sponsr.setState("first");
  sponsr.setState("second");
  manager.addMemo(sponsr.saveAsMemo());
  sponsr.setState("second");
  manager.addMemo(sponsr.saveAsMemo());
  std::cout<<manager.getMemo(0).getState()<<std::endl;
  std::cout<<manager.getMemo(1).getState()<<std::endl;
}