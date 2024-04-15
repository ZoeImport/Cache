#include <iostream>

// 状态接口
class OrderState {
public:
  virtual void handle() const = 0;
};

// 具体状态类：待支付状态
class PendingPaymentState : public OrderState {
public:
  void handle() const override {
    std::cout << "Order is pending payment." << std::endl;
  }
};

// 具体状态类：已支付状态
class PaidState : public OrderState {
public:
  void handle() const override { std::cout << "Order is paid." << std::endl; }
};

// 具体状态类：已发货状态
class ShippedState : public OrderState {
public:
  void handle() const override {
    std::cout << "Order is shipped." << std::endl;
  }
};

// 具体状态类：已完成状态
class CompletedState : public OrderState {
public:
  void handle() const override {
    std::cout << "Order is completed." << std::endl;
  }
};

// 上下文类
class Order {
private:
  OrderState *currentState;

public:
  Order() : currentState(new PendingPaymentState()) {}

  void setState(OrderState *newState) { currentState = newState; }

  void processOrder() const { currentState->handle(); }
};

int main() {
  Order order;

  order.processOrder(); // Output: Order is pending payment

  order.setState(new PaidState());
  order.processOrder(); // Output: Order is paid

  order.setState(new ShippedState());
  order.processOrder(); // Output: Order is shipped

  order.setState(new CompletedState());
  order.processOrder(); // Output: Order is completed

  return 0;
}
