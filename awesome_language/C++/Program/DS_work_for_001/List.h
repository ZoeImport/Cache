#ifndef _LIST_H_
#define _LIST_H_

#include <iostream>
#include <stdexcept>
#include <vector>

template <typename T>
class Node
{
public:
  T data;
  Node *next;

  Node(const T &newData) : data(newData), next(nullptr) {}
};

template <typename T>
class LinkedList
{
private:
  Node<T> *head;

public:
  LinkedList() : head(nullptr) {}

  ~LinkedList() { clear(); }

  // 在链表末尾添加元素
  void append(const T &value)
  {
    Node<T> *newNode = new Node<T>(value);

    if (head == nullptr)
    {
      head = newNode;
    }
    else
    {
      Node<T> *current = head;
      while (current->next != nullptr)
      {
        current = current->next;
      }
      current->next = newNode;
    }
  }

  // 在链表开头插入元素
  void prepend(const T &value)
  {
    Node<T> *newNode = new Node<T>(value);
    newNode->next = head;
    head = newNode;
  }

  // 删除指定值的元素
  void remove(const T &value)
  {
    if (head == nullptr)
    {
      return;
    }

    if (head->data == value)
    {
      Node<T> *temp = head;
      head = head->next;
      delete temp;
      return;
    }

    Node<T> *current = head;
    while (current->next != nullptr && current->next->data != value)
    {
      current = current->next;
    }

    if (current->next != nullptr)
    {
      Node<T> *temp = current->next;
      current->next = current->next->next;
      delete temp;
    }
  }

  // 查找指定值的元素，并返回其地址
  Node<T> *find(const T &value) const
  {
    Node<T> *current = head;
    while (current != nullptr)
    {
      if (current->data == value)
      {
        return current;
      }
      current = current->next;
    }
    return nullptr;
  }

  // 修改指定值的元素
  void modify(const T &oldValue, const T &newValue)
  {
    Node<T> *nodeToModify = find(oldValue);
    if (nodeToModify != nullptr)
    {
      nodeToModify->data = newValue;
    }
  }

  // 清空链表
  void clear()
  {
    Node<T> *current = head;
    while (current != nullptr)
    {
      Node<T> *temp = current;
      current = current->next;
      delete temp;
    }
    head = nullptr;
  }

  // 打印链表元素
  void print() const
  {
    Node<T> *current = head;
    while (current != nullptr)
    {
      std::cout << current->data << " ";
      current = current->next;
    }
  }

  std::vector<T> &forEach(std::vector<T> &arr) const
  {
    Node<T> *current = head;
    while (current != nullptr)
    {
      arr.emplace_back(current->data);
      current = current->next;
    }
    return arr;
  }
};

#endif