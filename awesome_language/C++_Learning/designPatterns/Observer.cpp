#include <algorithm>
#include <iostream>
#include <list>
class Observer {
  public:
  virtual void update(const std::string&msg)=0;
};


class Subscriber:public Observer {
public:
  Subscriber() = default;
  Subscriber(std::string name) : name(name){};
  void update(const std::string &msg) override {
    std::cout<<this->name<<",please see this new:"<<msg<<std::endl;
  }
  private:
    std::string name;
};

class Subject {
public:
  auto indexof(Observer *observer) {
    auto it=std::find(observerList.begin(),observerList.end(),observer);
    return it;
  }
  bool attach(Observer *observer) {
    if (indexof(observer)==observerList.end()) {
      this->observerList.push_back(observer);
      return true;
    }
    return false;
    }
    bool dettch(Observer *observer) {
      auto temp=indexof(observer);
      if (temp==observerList.end()) {
        return false;
      }
      observerList.erase(temp);
      return true;
    }
    void setNews(std::string msg) { this->news = msg; }
    std::string getNews() {
      return this->news;
    }
  virtual void notify()=0;
protected:
  std::list<Observer *> observerList;
  std::string news;
};

class Publisher:public Subject {
public:
  Publisher() = default;
  void notify() override {
    for (auto x : this->observerList) {
      x->update(this->news);
    }
  }

};

int main() {
Subscriber *tom=new Subscriber("Tom");
Subscriber *tommy = new Subscriber("tommy");
Publisher *publisher = new Publisher;

publisher->attach(tom);
publisher->attach(tommy);

publisher->setNews("2012 end of world");
publisher->notify();
}

