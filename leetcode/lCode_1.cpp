#include <iostream>
#include <map>
#include <unordered_map>
#include <utility>
#include <vector>
using namespace std;

namespace lCode {
    auto twoSum1(vector<int>& array,int target){
        map<int,int>mp;
        auto index=0;
        vector<int>res;
        for (auto num :array) {
            mp.insert(make_pair(num,index));
            index++;
        }
        index=0;
        for (auto num :array) {
            if (mp.find(target - num)->second) {
                res.push_back(index);
                res.push_back(mp.find(target-num)->second);
                return res;
            }
            index++;
        }
        return res;
    }
    auto twoSum2(vector<int> &array, int target) {
        unordered_map<int, int> mp;
        auto index = 0;
        for (auto num : array) {
            mp.insert(make_pair(num, index));
            if (mp.find(target - num) != mp.end() &&
                    mp.find(target - num)->second!=index) {
                return vector<int>() = {mp.find(target - num)->second, index};
            }
            index++;
        }
        return vector<int>(1,-1);
}
    }
int main(){
    for (auto num : lCode::twoSum2(vector<int>() = {3,2,4}, 6)) {
            cout << num << " ";
    }
}