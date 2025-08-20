
#include "OpenAddressHashTable.h"
#include "UserInfo.h"
#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <utility>

int OpenAddressHashTable::hashFunction(int Key) { return Key % TABLE_SIZE; }

int OpenAddressHashTable::insert(int Key, UserInfo &Value)
{
  int index = hashFunction(Key);
  while (!table[index].second.isEmpty())
  {
    index = (index + 1) % TABLE_SIZE;
  }
  table[index] = std::make_pair(Key, Value);
  return 0;
}

UserInfo OpenAddressHashTable::get(int Key)
{
  int index = hashFunction(Key);
  while (!table[index].first && table[index].first != Key)
  {
    index = (index + 1) % TABLE_SIZE;
  }
  if (!table[index].first && table[index].first != Key)
    return table[index].second;
  return UserInfo();
}

UserInfo &OpenAddressHashTable::operator[](int Key)
{

  int index = hashFunction(Key);
  auto OriginIndex = index;
  while (!table[index].second.isEmpty())
  {
    if (table[index].first == Key)
    {
      return table[index].second;
    }
    index = (index + 1) % TABLE_SIZE;
    if (index == OriginIndex)
    {
      throw std::out_of_range("table is full !!!");
    }
  }
  table[index] = std::make_pair(Key, UserInfo());
  return table[index].second;
}

// OpenAddressHashTable& initOpenAddressHashTableByPhoneNumber(std::ifstream& ifs, OpenAddressHashTable &hashTable,std::vector<UserInfo>& user_info_list_phoneNumber){
//     readUserInfo(ifs,user_info_list_phoneNumber);
//     for (auto atom :user_info_list_phoneNumber) {
//         hashTable[strToInt(atom.getPhoneNumber())]=atom;
//     }
//     return hashTable;
// }
// OpenAddressHashTable& initOpenAddressHashTableByUserName(std::ifstream& ifs, OpenAddressHashTable &hashTable,std::vector<UserInfo>& user_info_list_userName){
//     readUserInfo(ifs,user_info_list_userName);
//     for (auto atom :user_info_list_userName) {
//         hashTable[strToInt(atom.getUserName())]=atom;
//     }
//     return hashTable;
// }

void OpenAddressHashTable::getAllUserInfos()
{
  for (auto atom : table)
  {
    std::cout << atom.first << "|" << atom.second << std::endl;
  }
}