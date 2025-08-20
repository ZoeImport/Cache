#include <cstdlib>
#include <iostream>
#include <ostream>
#include <stdexcept>
#include <string>
#include <type_traits>
using namespace std;
class Animal {
public:
  Animal(int age, char gender, char size) {
    m_age = age;
    m_gender = gender;
    m_size = size;
  }

  int getAge() { return m_age; }
  void setAge(int age) { m_age = age; }

  char getGender() { return m_gender; }
  void setGender(char gender) { m_gender = gender; }

  char getSize() { return m_size; }
  void setSize(char size) { m_size = size; }

private:
  int m_age;
  char m_gender;
  char m_size;
};

ostream &operator<<(ostream &cout, Animal &dog) {
  cout << dog.getAge() << dog.getGender() << dog.getSize() << endl;
  return cout;
}

class Person {
private:
  int age;
  char gender;
  string name;

public:
  virtual void work() { cout << this->name << " is working..." << endl; };
  Person(){};
  Person(int age,char gender,string name):age(age),gender(gender),name(name){};
  int getAge() { return age; }
  void setAge(int age) { this->age = age; }
  char getGender() { return gender; }
  void setGender(char gender) { this->gender = gender; }
  string getName() { return name; }
  void setName(string name) { this->name = name; }

  void showInfo() { cout << age << endl << gender << endl << name << endl; }
};

class Teacher : public Person {
private:
  int s;

public:
  void work() { cout << this->getName() << " is teaching " << this->s << endl; }
  int getS() { return s; }
  void setS(int s) { this->s = s; }

  // Ming En
  // Ming is teaching En...
};
ostream &operator<<(ostream &cout, Person &p) {
  cout << p.getAge() << p.getGender() << p.getName() << endl;
  return cout;
}

class Student : public Person {
public:
    int score;
    Student(int age,char gender,string name,int score):Person(age,gender,name),score(score){};
    virtual void work(){
        cout<<this->getName()<<" is learning..."<<endl;
    }
};
template <class T> void swop(T &a, T &b);

template <class T> class Value {
public:
  Value<T>(T value):value(value){};
  T value;
};
template <class T> ostream &operator<<(ostream &cout, Value<T> &v) {
  cout << v.value << endl;
  return cout;
}

struct Node{
    // 指针域
    Node * next;
    // 数据域
    int data;
};
void init_Node(Node*&node){
    node->next=nullptr;
}
void insert(Node *&node,int value){
    Node*  newNode=new Node;
    newNode->data=value;
    if (!node->next) {
        node->next=newNode;
    }else {
        newNode->next=node->next;
        node->next=newNode;
    }
}
bool deleteNode(Node *&node,int value){
    if (!node->next) {
        return false;
    }else {
        Node *p=node->next;
        while (p) {
            if (p->next->data==value) { 
              break;
            }
            p=p->next;
        }
        Node *q=p->next;
        p->next=q->next;
        delete (q);
        return true;
    }
}

int  forEach(Node *node){
    Node *p=node->next;
    int count =1;
    while (p) {
        cout<<count++<<" : "<<p->data<<endl;
        p=p->next;
    }
    return count;
}


int main() {

  Value<int> three(3);
  cout << three.value << endl;
  Value<char> ch('s');
  cout << ch.value << endl;
  cout << "ch: " << ch << endl;
  cout << "===================================" << endl;
  Animal dog(3, 'm', 's');
  cout << dog.getAge() << endl;
  Person p;
  p.setAge(18);
  p.setGender('w');
  p.setName("Ming");

  p.showInfo();
  p.work();
  Teacher t;
  t.setName("Ming");
  t.setS(1);
  t.work();

  cout << dog;
  cout << p;

  char s = 's';
  char m = 'm';

  swop(s, m);
  cout << s << m << endl;
}

template <class T> void swop(T &a, T &b) {
  T temp = a;
  a = b;
  b = temp;
}
