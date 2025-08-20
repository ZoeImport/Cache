//算法介绍

#include <algorithm>
#include <iostream>
#include <iterator>
#include <ostream>
#include <vector>
#include <functional>
#include <numeric>
//numeric accumulate fill
using namespace std;
void myPrint(int val){
    cout<<val<<" ";
}
int Transform(int val){
    return val+1000;
}
int myCompareOne(int val){
    return val>2;
}
class myComp{
    public:
        int operator()(int val){
            return val>2;
        }
};
int main(){
    vector<int>v1;
    v1.push_back(3);
    v1.push_back(2);
    v1.push_back(1);
    v1.push_back(4);
    v1.push_back(6);
    v1.push_back(6);

    //遍历
    for_each(v1.begin(),v1.end(),myPrint);
    cout<<endl;
    cout<<"=========================================================="<<endl;
    vector<int>v2;
    v2.resize(v1.size());
    transform(v1.begin(),v1.end(),v2.begin(),Transform);
    for (auto num :v2) {
        cout<<num<<" ";
    }


    //查找算法
    //find
    auto it1=find(v1.begin(),v1.end(),100);
    cout<<*it1<<endl;
    //find_if
    auto it2=find_if(v1.begin(),v1.end(),myCompareOne);
    cout<<*it2<<endl;
    //adjacent_find
    auto it3=adjacent_find(v1.begin(),v1.end());
    cout<<*it3<<endl;
    //binary_search
    sort(v1.begin(),v1.end());
    auto bool1=binary_search(v1.begin(),v1.end(),3);
    cout<<bool1<<endl;
    //count
    auto ct1=count(v1.begin(),v1.end(),6);
    cout<<ct1<<endl;
    //count_if
    auto ct2=count_if(v1.begin(),v1.end(),myCompareOne);
    cout<<ct2<<endl;
    //sort
    sort(v2.begin(),v2.end());
    //random_shuffle
    // shuffle(v1.begin(), v1.end() )在c++17中被完全移除


    //merge
    vector<int>v3(v1);
    vector<int>v4(v1);
    vector<int>v5;
    v5.resize(v3.size()+v4.size());
    merge(v3.begin(),v3.end(),v4.begin(),v4.end(),v5.begin());
    for (auto num : v5) {
        cout<<num<<" ";
    }
    cout<<endl;
    //reverse
    reverse(v5.begin(),v5.end());
    for (auto num :v5) {
        cout<<num<<" ";
    }
    cout << endl;
    //copy
    vector<int>v6;
    v6.resize(v5.size());
    copy(v5.begin(),v5.end(),v6.begin());
    for (auto num :v6) {
        cout<<num<<" ";
    }
    cout << endl;
    //replace
    replace(v6.begin(),v6.end(),1,1000);
    for (auto num : v6) {
        cout<<num<<" ";
    }
    cout<<endl;
    //replace_if
    replace_if(v6.begin(),v6.end(),myComp(),23232);
    for (auto num : v6) {
        cout << num << " ";
    }
    cout << endl;
    //swap
    swap(v1,v6);
    //accumulate
    auto sumInt=accumulate(v1.begin(),v1.end(),0);
    cout<<sumInt<<endl;
    //fill
    fill(v6.begin(),v6.end(),666);
    for (auto num :v6) {
        cout<<num<<" ";
    }
    //set_intersection
    //交集
    vector<int>v7;
    v7.push_back(7);
    v7.push_back(7);
    v7.push_back(7);
    v7.push_back(7);
    vector<int>v8(v7);
    vector<int>v9(v8.size());
    vector<int>v10(v8.size());
    vector<int>v11(v8.size());
    set_intersection(v7.begin(),v7.end(),v8.begin(),v8.end(),v9);
    for (auto num :v9) {
        cout<<num<<" ";
    }
    cout<<endl;
    //set_union
    set_union(v7.begin(), v7.end(), v8.begin(), v8.end(), v10);
    for (auto num :v10) {
        cout<<num<<" ";
    }
    cout<<endl;
    //set_difference
    set_difference(v7.begin(), v7.end(), v8.begin(), v8.end(), v11);
    for (auto num : v11) {
        cout << num << " ";
    }
    cout << endl;
}