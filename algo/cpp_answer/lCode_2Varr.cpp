#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

namespace lCode {
  /*
  如果长度为一直接进行返回
  对原数组进行排序
  创建一个新二维数组，将原数组的第0组直接放入新数组的0索引，将ans_index记为比较过程中答案数组的索引，srs_index记为比较过程中原数组的索引
  如果前一个的end>=后一个的start,合并二者并存入新数组，再将其跟下一位同样比较
  如果没有交集就按序复制并将最后复制进的与原数组的下一个进行判断

  
  */
vector<vector<int>> merge(vector<vector<int>> &intervals) {
  if (intervals.size() <= 1) {
    return intervals;
  }

  // 对原数组按区间的起点进行排序
  sort(intervals.begin(), intervals.end(),
       [](const vector<int> &a, const vector<int> &b) { return a[0] < b[0]; });

  vector<vector<int>> merged;
  merged.push_back(intervals[0]);

  for (int i = 1; i < intervals.size(); i++) {
    if (merged.back()[1] >= intervals[i][0]) {
      // 如果当前区间与上一个区间有重叠，合并它们
      merged.back()[1] = max(merged.back()[1], intervals[i][1]);
    } else {
      // 否则，将当前区间加入结果
      merged.push_back(intervals[i]);
    }
  }

  return merged;
}

} // namespace lCode

int main() {
  /*
  输入：intervals = [[1,3],[2,6],[8,10],[15,18]]
  输出：[[1,6],[8,10],[15,18]]
  解释：区间 [1,3] 和 [2,6] 重叠, 将它们合并为 [1,6].
  */
  vector<vector<int>> vt; 
  vt.push_back({1,3});
  vt.push_back({2,6});
  vt.push_back({8,10});
  vt.push_back({15,18});
  auto ans=lCode::merge(vt);
  for (auto row :ans) {
    cout<<"[";
    for (auto column :row) {
      cout<<column<<" ";
    }
    cout<<"]";
  }
}