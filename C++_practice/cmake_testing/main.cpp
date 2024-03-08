/*
  test for cmake obj build 
.
├── bulid
├── head
├── lib
├── main.cpp
└── src
    ├── divide.cpp
    ├── divide.h
    ├── minus.cpp
    ├── minus.h
    ├── multiply.cpp
    ├── multiply.h
    ├── plus.cpp
    └── plus.h
*/

#include <iostream>
#include "src/calcDir/divide.h"
#include "src/calcDir/minus.h"
#include "src/calcDir/multiply.h"
#include "src/calcDir/plus.h"

int main(){
  auto result=minus(10,5)*plus(20,10)*divide(10,5)*multiply(5,5);
  std::cout<<"result : "<<result;
}