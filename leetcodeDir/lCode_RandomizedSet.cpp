#include <cstdlib>
#include <iostream>
#include <unordered_map>
#include <vector>

class RandomizedSet {
public:
  RandomizedSet() {}

  bool insert(int val) {
    if (map.count(val)) {
      return false;
    }
    int last = nums.size();
    nums.push_back(val);
    map[val] = last;
    return true;
  }
  bool remove(int val) {
    if (!map.count(val)) {
      return false;
    }
    int index = map[val];
    int last = nums.back();
    nums[index] = last;
    map[last] = index;
    nums.pop_back();
    map.erase(val);
    return true;
  }

  int getRandom() { return nums[rand() % nums.size()]; }

private:
  std::vector<int> nums;
  std::unordered_map<int, int> map;
};

int main() { std::cout << "ok"; }