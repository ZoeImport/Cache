#include <iostream>
#include <vector>
using namespace std;

namespace lCode {
auto findDiagonalOrder1(vector<vector<int>> &mat) {
  vector<int> answer;
  if (mat.size() * mat[0].size() == 1 || mat.empty())
    return answer;
  auto current_column = 0;
  auto current_row = 0;
  // 将第一个元素直接存入
  answer.push_back(mat[current_row][current_column++]);
  answer.push_back(mat[current_row++][current_column--]);
  // 方向依据奇偶性判断
  auto turns = mat.size() + mat[0].size() - 1;
  for (auto i = 1; i < turns; i++) {

    if (i <= (turns / 2) + 1) {
      // 前半段遍历
      // 奇数右上
      // 未达至上边界
      if (i % 2) {
        while (current_row != 0) {
          answer.push_back(mat[current_row--][current_column++]);
        }
        current_column++;
      } else {
        // 偶数左下
        while (current_column != 0) {
          answer.push_back(mat[current_row++][current_column--]);
        }
        current_row++;
      }
    } else {
      // 后半段遍历
      // 奇数右上
      if (i % 2) {
        while (current_column != mat[0].size()) {
          answer.push_back(mat[current_row--][current_column++]);
        }
        current_row++;
      } else {
        // 偶数左下
        while (current_row != mat.size()) {
          answer.push_back(mat[current_row++][current_column--]);
        }
        current_column++;
      }
    }
  }
  //   if (i==0) {
  //     answer.push_back(mat[0][0]);
  //     current_column++;
  //   }else{
  //     if (i % 2) {
  //       // 为奇数，向右上
  //       if (i < (turns / 2) + 1) {
  //         while (current _row) {
  //           answer.push_back(mat[current_row--][current_column++]);
  //         }
  //         // 一轮遍历完毕后变向,更换起点
  //         current_column++;
  //       } else {
  //         while (current_column != mat[0].size()) {
  //           answer.push_back(mat[current_row--][current_column++]);
  //         }
  //         current_row++;
  //       }
  //     } else {
  //       // 为偶数，向左下
  //       if (i < (turns / 2) + 1) {
  //         while (current_column) {
  //           answer.push_back(mat[current_row++][current_column--]);
  //         }
  //         current_row++;
  //       } else {
  //         while (current_row != mat.size()) {
  //           answer.push_back(mat[current_row++][current_column--]);
  //         }
  //         current_column++;
  //       }
  //     }
  //   }
  // }
  return answer;
}
vector<int> findDiagonalOrder2(vector<vector<int>> &mat) {
  vector<int> result;
  if (mat.empty() || mat[0].empty()) {
    return result;
  }

  int m = mat.size();
  int n = mat[0].size();
  int totalElements = m * n;
  bool goingUp = true;

  for (int i = 0; i < totalElements; ++i) {
    result.push_back(
        mat[(goingUp) ? (i < m ? i : m - 1) : (i < n ? 0 : i - n + 1)]
           [(goingUp) ? (i < m ? 0 : i - m + 1) : (i < n ? i : n - 1)]);
    int row = (goingUp) ? (i < m ? i : m - 1) : (i < n ? 0 : i - n + 1);
    int col = (goingUp) ? (i < m ? 0 : i - m + 1) : (i < n ? i : n - 1);

    while (row >= 0 && row < m && col >= 0 && col < n) {
      result.push_back(mat[row][col]);
      row += (goingUp) ? -1 : 1;
      col += (goingUp) ? 1 : -1;
    }

    goingUp = !goingUp;
  }

  return result;
}

vector<int> findDiagonalOrder(vector<vector<int>> &mat) {
  vector<int> res;
  res.push_back(mat[0][0]);
  int m = mat.size(); // 总行列数
  int n = mat[0].size();
  int row = 0; // 行列下标
  int column = 0;
  while (true) {
    // 判断是否遍历到最后一位
    if (row == m - 1 && column == n - 1)
      break;
    // 往右上遍历
    while (row != 0 && column != n - 1) // 右上能走，循环右上
    {
      row--;
      column++;
      res.push_back(mat[row][column]);
    }
    if (row == 0 && column != n - 1) // 到第一行，非最后一列：列下标+1
      column++;
    else // 其他情况：行下标+1
      row++;
    res.push_back(mat[row][column]);

    // 判断是否遍历到最后一位
    if (row == m - 1 && column == n - 1)
      break;
    // 往左下遍历
    while (row != m - 1 && column != 0) // 左下能走，循环左下
    {
      row++;
      column--;
      res.push_back(mat[row][column]);
    }
    if (row != m - 1 && column == 0) // 到第一列，非最后一行：行下标+1
      row++;
    else // 其他情况：列下标+1
      column++;
    res.push_back(mat[row][column]);
  }
  return res;
}
} // namespace lCode

int main() {
  //[[1,1,1],[1,0,1],[1,1,1]]
  vector<vector<int>> matrix;
  matrix.push_back({1, 2, 3});
  matrix.push_back({4, 5, 6});
  matrix.push_back({7, 8, 9});
  for (auto num : lCode::findDiagonalOrder(matrix)) {
    cout << num << " ";
  }
}