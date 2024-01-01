#ifndef _HASH_TABLE_CHINING
#define _HASH_TABLE_CHINING

#include <fstream>
#include <list>
#include <utility>
#include <vector>
#include <string>
#include "UserInfo.h"

class HashTable
{
public:
  HashTable() : table(TableSize){};
  int hashFUnction(int index);
  int insert(int key, const UserInfo &value);
  UserInfo get(int key);
  UserInfo &operator[](int key);
  std::vector<UserInfo> getAllUserInfo();
  // UserInfo& operator[](std::string key);

private:
  static const int TableSize = 90;
  std::vector<std::list<std::pair<int, UserInfo>>> table;
};

// HashTable& initHashTableByPhoneNumber(std::ifstream& ifs, HashTable &hashTable,std::vector<UserInfo>& user_info_list);
// HashTable& initHashTableByUserName(std::ifstream& ifs, HashTable &hashTable,std::vector<UserInfo>& user_info_list);

#endif