#include <algorithm>
#include <iostream>
#include <iterator>
#include <stdexcept>
#include <vector>

using namespace std;

namespace lCode {
    auto minCostClimbingStairs(vector<int> &cost){
        auto len=cost.size();
        vector<int> step_cost(len+1);
        step_cost[0]=step_cost[1]=0;
        for (auto index=2;index<=len;++index) {
          step_cost[index] = min(step_cost[index - 1] + cost[index - 1],
                                 step_cost[index - 2] + cost[index - 2]);
        }
        return step_cost[len];
    }

    auto minCostClimbingStairs2(vector<int> &cost){
        auto len=cost.size();
        auto prev=0,curr=0,next=0;
        for (auto index=0;index<=len;++index) {
            next=min(prev+cost[index-2],curr+cost[index-1]);
            prev=curr;
            curr=next;
        }
        return curr;
    }
}

int main(){
        vector<int> cost = { 1, 100, 1, 1, 1, 100, 1, 1, 100, 1 };
        cout<<lCode::minCostClimbingStairs(cost)<<endl;
}