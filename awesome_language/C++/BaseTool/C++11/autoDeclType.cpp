#include <iostream>
using namespace std;
template <class T>
auto add( T val1,T val2)->decltype(val1+val2){
    return val1+val2;
}

int main(){
    auto &&res1=add(1, 3);
    res1++;
    cout<<res1<<endl;
}