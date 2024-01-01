#ifndef _ORDER_STACK_
#define _ORDER_STACK_

#include "ClothesOrder.h"
#include <iostream>
#include <stdexcept>
#include <vector>

// 订单栈头文件

template <typename T>
class Stack
{
public:
  // 增加元素
  void push(const T &value) { data.push_back(value); }

  // 删除元素
  void pop()
  {
    if (empty())
    {
      throw std::out_of_range("Stack is empty");
    }
    data.pop_back();
  }

  // 获取栈顶元素
  T &top()
  {
    if (empty())
    {
      throw std::out_of_range("Stack is empty");
    }
    return data.back();
  }

  // 栈是否为空
  bool empty() const { return data.empty(); }

  // 获取栈的大小
  size_t size() const { return data.size(); }

  // 查找元素（返回索引）
  int find(const T &value) const
  {
    for (int i = data.size() - 1; i >= 0; --i)
    {
      if (data[i] == value)
      {
        return i;
      }
    }
    return -1; // 未找到
  }

  // 修改元素
  void modify(int index, const T &value)
  {
    if (index < 0 || index >= data.size())
    {
      throw std::out_of_range("Index out of range");
    }
    data[index] = value;
  }

  // 打印栈中元素
  void print() const
  {
    for (const auto &element : data)
    {
      std::cout << element << " ";
    }
    std::cout << std::endl;
  }

private:
  std::vector<T> data;
};
#endif