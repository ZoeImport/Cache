#include <iostream>

class Node {
public:
  Node *next;
  int data;

  Node(int data) : data(data), next(nullptr) {}
};

class Iterator;

class SingleList {
public:
  SingleList() : head(nullptr) {}
  void append(int val) {
    Node *newNode = new Node(val);
    if (head == nullptr) {
      head = newNode;
    } else {
      Node *curr = head;
      while (curr->next != nullptr) {
        curr = curr->next;
      }
      curr->next = newNode;
    }
    ++count;
    // std::cout << val << std::endl;
  }
  bool isOver() { return head == nullptr; }
  int getCount() { return this->count; }

  Node *getHead() { return this->head; }

  Iterator *getIterator();

private:
  Node *head;
  int count;
};

class Iterator {
public:
  Iterator(SingleList *list) : list(list), curr(list->getHead()) {
    // std::cout << "curr ptr init:" << curr->data << std::endl;
  }
  Node *getCurr() { return curr; }
  virtual Node *first() = 0;
  virtual Node *next() = 0;
  virtual bool hasNext() = 0;

protected:
  SingleList *list;
  Node *curr;
};

class ListIterator : public Iterator {
public:
  using Iterator::Iterator;
  Node *first() override {
    this->curr = this->list->getHead();
    return this->curr;
  }
  Node *next() override {
    this->curr = this->curr->next;
    return this->curr;
  }

  bool hasNext() override { return !((this->curr) == nullptr); }
};

Iterator *SingleList::getIterator() { return new ListIterator(this); }

int main() {
  SingleList *list = new SingleList;
  list->append(3);
  list->append(4);
  list->append(5);

  Iterator *it = list->getIterator();
  Node *node = it->first();
  while (it->hasNext()) {
    std::cout << node->data << " ";
    node = it->next();
  }
}