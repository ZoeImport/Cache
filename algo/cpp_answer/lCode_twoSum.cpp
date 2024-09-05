#include <iostream>
#include <vector>

using namespace std;

namespace lCode {
    auto twoSum(vector<int>& numbers,int target){
        auto start=0;
        auto end = static_cast<int>(numbers.size() - 1);
        while(start<end) {
            if (numbers[start]+numbers[end]==target) {
                return vector<int>{start+1,end+1};
            }
            numbers[start]+numbers[end]>target?--end:start++;
        }
        return vector<int>{-1};
    }
}

int main(){
    auto numbers=vector<int>{2,3,4};
    for (auto num :lCode::twoSum(numbers,6)) {
        cout<<num<<" ";
    }
}