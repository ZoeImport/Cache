猪的笔记

# 编译

C++是高级程序语言，编译器负责把高级程序语言编译为汇编语言，最后再把汇编语言转换为机器语言



```c++
#include<iostream>
struct Node{
    int data;
    Node* head;
};
struct Num {
    int data; 
};
void initNode(Node*list){
    list->head=nullptr;
}

bool isEmpty(Node* list){
    if(list->head==nullptr)
        return true;
    return false;
}

void insertNode(Node*list,int data){
    if(isEmpty(list)){
        Node* newNode=new Node;
        newNode->data=data;
        list->head=newNode;
    }
    // else 
}



int main(){
    Num no1;
    no1.data=20;
    std::cout<<no1.data<<std::endl;
    Node *list;
    insertNode(list,no1.data);
    std::cout<<list->head->data<<std::endl;
return 0;
}
```

小猪佩奇