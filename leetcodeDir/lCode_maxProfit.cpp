#include <iostream>
#include <vector>

using namespace std;

int maxProfit(vector<int> &prices) {
  int len = prices.size();
  if(len==2&&prices[0]>=prices[1])return 0;
  auto slow=len-1;
  auto fast=slow-1;
  auto ans=0;
  while (slow>=0) {
    if(prices[slow]>prices[fast]){
      if(prices[slow]-prices[fast]>ans){
        ans=prices[slow]-prices[fast];
      }
        --fast;
    }else {
      slow=fast;
      --fast;
    }
  }
  return ans;
}

int main() {


}
