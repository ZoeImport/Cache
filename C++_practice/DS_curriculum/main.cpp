#include <fstream>
#include <iostream>
#include <unordered_set>
#include <utility>
#include <vector>
#include "UserInfo.h"
#include "HashTable.h"
#include "OpenAddressHashTable.h"
#include "App.h"
// #include "App.cpp"

using namespace std;
int main()
{
  string filePath("../user_info.txt"); // 用户信息文件路径
  //  AppFunction(filePath);
  // AppFunctionOpen(filePath);
  APP<OpenAddressHashTable>(filePath);
}
