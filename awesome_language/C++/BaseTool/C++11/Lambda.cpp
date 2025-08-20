#include <iostream>
using namespace std;

int main(){
    auto myPrint=[](int a){
        cout<<a<<" ";
    };
    myPrint(1);
}