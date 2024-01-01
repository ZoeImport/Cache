#ifndef _OPEN_ADDRESS_HASH_TABLE
#define _OPEN_ADDRESS_HASH_TABLE

#include "UserInfo.h"
#include <cstddef>
#include <string>
#include <utility>
#include <vector>

class OpenAddressHashTable
{
public:
  OpenAddressHashTable() : table(TABLE_SIZE){};
  int hashFunction(int Key);
  int insert(int Key, UserInfo &Value);
  UserInfo &operator[](int Key);
  UserInfo get(int Key);
  void getAllUserInfos();

private:
  std::vector<std::pair<int, UserInfo>> table;
  const int static TABLE_SIZE = 90;
};

// OpenAddressHashTable &
// initOpenAddressHashTableByPhoneNumber(std::ifstream &ifs,
//                                       OpenAddressHashTable &hashTable,
//                                       std::vector<UserInfo> &user_info_list);
// OpenAddressHashTable &
// initOpenAddressHashTableByUserName(std::ifstream &ifs,
//                                    OpenAddressHashTable &hashTable,
//                                    std::vector<UserInfo> &user_info_list);

#endif