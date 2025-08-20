#include <iostream>

class Strategy {
public:
  virtual void payStrategy(int count)=0;
};

class WechatPay : public Strategy {
public:
  void payStrategy(int count) override {
    std::cout<<"Pay by method WechatPay: trade "<<count<<"$"<<std::endl;
  }
};

class AliPay : public Strategy {
public:
  void payStrategy(int count) override {
    std::cout<<"Pay by method AliPay: trade "<<count<<"$"<<std::endl;
  }
};

class PaymentContext {
public:
  PaymentContext()=default;
  void setPayStrategy(Strategy *strategy) { this->strategy = strategy; }
  bool excutePay(int count) {
    if (strategy==nullptr) {
      std::cout<<"without legal pay strategy"<<std::endl;
      return false;
    }else {
      this->strategy->payStrategy(count);
      return true;
    }
  }
private:
  Strategy *strategy;
};

int main() {
  Strategy * wechat=new WechatPay;
  Strategy *ali = new AliPay;
  PaymentContext context;
  context.setPayStrategy(wechat);
  context.excutePay(20);
}