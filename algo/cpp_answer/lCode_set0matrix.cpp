#include <iostream>
#include <set>
#include <unordered_map>
#include <vector>
using namespace std;

namespace lCode {
    void setZeroes2(vector<vector<int>> &matrix) {
        set<int>zeroLocations;
        auto matrix_row=0;
        auto hasZero = false;
        for (auto &arr :matrix) {
            for (int i=0 ;i<arr.size();i++) {
                
                if(!arr[i]){
                    zeroLocations.insert(i);
                    hasZero=true;
                }
            }
            if (hasZero) {
                arr = vector<int>(arr.size(), 0);
            }            
            matrix_row++;
            hasZero=false;
        } 
        for (auto &column :zeroLocations) {
            for (auto &arr :matrix) {
                arr[column]=0;
            }
        }
    }
    void setZeroes(vector<vector<int>> &matrix) {
        int numRows = matrix.size();
        int numCols = matrix[0].size();

        // 用于记录包含零的行和列
        vector<bool> zeroRows(numRows, false);
        vector<bool> zeroCols(numCols, false);

        // 遍历矩阵，找到包含零的行和列
        for (int i = 0; i < numRows; i++) {
            for (int j = 0; j < numCols; j++) {
                if (matrix[i][j] == 0) {
                    zeroRows[i] = true;
                    zeroCols[j] = true;
                }
            }
        }

        // 根据记录的结果将对应行和列设置为零
        for (int i = 0; i < numRows; i++) {
            for (int j = 0; j < numCols; j++) {
                if (zeroRows[i] || zeroCols[j]) {
                    matrix[i][j] = 0;
                }
            }
        }
    }
}

int main(){
        //[[1,1,1],[1,0,1],[1,1,1]]
    vector<vector<int>> matrix;
    matrix.push_back({1,1,1});
    matrix.push_back({1,0,1});
    matrix.push_back({1,1,1});
    lCode::setZeroes2(matrix);
    for (auto arr :matrix) {
        cout<<"[ ";
        for (auto num :arr) {
            cout<<num<<" ";
        }
        cout<<"]"<<endl;
    }

}