#include <iostream>
#include <memory>

class Handler {
protected:
  std::shared_ptr<Handler> nextHandler;
  std::string host;

public:
  virtual void handleReq(const std::string &host) = 0;
  void setNextHandler(std::shared_ptr<Handler> handler) {
    this->nextHandler = handler;
  }
};

// 1.1.1.1
class SubHandler1 : public Handler {
public:
  SubHandler1() {
    this->host = "1.1.1.1";
    std::cout << "host init:" << this->host << std::endl;
  }
  void handleReq(const std::string &host) override {
    if (host == this->host) {
      std::cout << "Req success..." << std::endl;
    } else {
      std::cout << "jump to next handler" << std::endl;
      this->nextHandler->handleReq(host);
    }
  }
};
// 2.2.2.2
class SubHandler2 : public Handler {
public:
  SubHandler2() {
    this->host = "2.2.2.2";
    std::cout << "host init:" << this->host << std::endl;
  }
  void handleReq(const std::string &host) override {
    if (host == this->host) {
      std::cout << "Req success..." << std::endl;
    } else {
      std::cout << "jump to next handler" << std::endl;
      this->nextHandler->handleReq(host);
    }
  }
};
// 3.3.3.3
class SubHandler3 : public Handler {
public:
  SubHandler3() {
    this->host = "3.3.3.3";
    std::cout << "host init:" << this->host << std::endl;
  }
  void handleReq(const std::string &host) override {
    if (host == this->host) {
      std::cout << "Req success..." << std::endl;
    } else {
      std::cout << "jump to next handler" << std::endl;
      this->nextHandler->handleReq(host);
    }
  }
};

int main() {
  auto handle1 = std::make_shared<SubHandler1>();
  auto handle2 = std::make_shared<SubHandler2>();
  auto handle3 = std::make_shared<SubHandler3>();
  handle1->setNextHandler(handle2);
  handle2->setNextHandler(handle3);
  handle1->handleReq("3.3.3.3");
}

