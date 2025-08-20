#include <iostream>
#include <ostream>
using namespace std;

template <class T>
class Value{
private:
T value;
public:
T getValue(){
    return value;
}
void setValue(T value){
    this->value=value;
}
Value()=default;

 Value(T value){
    this->value=value;
}

//重载++运算符
Value<T>& operator++(){
    this->value++;
    return *this;
}

Value<T>operator++(T){
    Value<T>temp=*this;
     this->value++;
    return temp;

}

Value<T> &operator--() {
    this->value--;
    return *this;
}

Value<T> operator--(T) {
    Value<T> temp = *this;
    this->value--;
    return temp;
}

bool operator==(Value<T>&value){
    return (this->value==value.value);
}
bool operator!=(Value<T>&value){
    return !(*this==value);
}

bool operator()(T b){
    return(this->value==b);
}



};
//重载<<运算符
template<class C>
ostream&operator<<(ostream&cout, Value<C>&&p){
    cout<<p.getValue()<<endl;
    return cout;
}

template <class T>
Value<T>  operator+(Value<T>&m,Value<T>&n){
    return ((m.getValue() + n.getValue()));
}
template <class T> Value<T> &operator-(Value<T> &m, Value<T> &n) {
    return (m.getValue() - n.getValue());
}

int main(){
    Value<int>p2(10);
    Value<int>p1=20;
    cout<<(p1==p2);
    cout<<(p1!=p2);
    cout<<(p1+p2);
    cout<<(p1(3));
}