//此处的ifndef endif 以及 define 用于防止重复定义的预编译指令 
#ifndef _Func_H
#define _Func_H

void swap_byme(int *num_1,int *num_2);

void showInfo(const Person *p);

int numSum(int num_1,int num_2);

int & showRef1();
int & showRef2();

void constRef(const int & num);

void defaultVoid(int num=16);

void overLoadVoid();
void overLoadVoid(int num);

void overloadFunc(int &num);
void overloadFunc(const int &num);

#endif