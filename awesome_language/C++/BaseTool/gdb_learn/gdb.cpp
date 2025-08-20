#include <iostream>
#include <vector>
using namespace std;
template<class parameterType>
auto myPrint(parameterType a,parameterType b)->decltype(a+b){
    return a+b;
}
int main(){
    cout<<myPrint(3,4)<<endl;;
    vector<int> v1;
    v1.push_back(5);
    v1.push_back(2);
    v1.push_back(0);
    
    auto *pv1=&v1;


    cout<<"over"<<endl;
    
}