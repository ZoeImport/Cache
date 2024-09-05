#include <any>
#include <iostream>
#include <utility>
#include <vector>
using namespace std;

namespace lCode {
// 矩阵旋转
void rotate(vector<vector<int>> &matrix) {
//   auto dimension = matrix.size();
  auto wheels = matrix.size() - 1;
  auto turns = matrix.size() / 2;
  auto vertex = make_pair(0, 0);
  while (turns) {
    // 外围控制每次旋转的圈位置
    for (auto offset = 0; offset < wheels; offset++) {
      // 内圈控制每圈旋转的几个元素的交换
      swap(matrix[vertex.first][vertex.second + offset],
           matrix[vertex.first + offset][vertex.second + wheels]);
      swap(matrix[vertex.first][vertex.second + offset],
           matrix[vertex.first + wheels - offset][vertex.second]);
      swap(matrix[vertex.first + wheels - offset][vertex.second],
           matrix[vertex.first + wheels][vertex.second + wheels - offset]);
    }
    --turns;
    wheels -= 2;
    vertex.first++;
    vertex.second++;
  }
}
} // namespace lCode
int main(){
  vector<vector<int>> matrix;
  matrix.push_back({1, 0, 1});
  matrix.push_back({1, 0, 1});
  matrix.push_back({1, 0, 1});
  lCode::rotate(matrix);
  for (auto arr : matrix) {
    cout << "[";
    for (auto num : arr) {
      cout << num << " ";
    }
    cout << "]" << endl;
  }
}