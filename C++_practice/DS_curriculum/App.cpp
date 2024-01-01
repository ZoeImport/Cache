#include "App.h"
#include "HashTable.h"
#include "OpenAddressHashTable.h"
#include "UserInfo.h"
#include <fstream>
#include <iostream>
#include <string>

int menuMsgOut()
{
  std::cout << "==========================" << std::endl;
  std::cout << "<欢迎使用电话号码查询系统>" << std::endl;
  std::cout << "==========================" << std::endl;
  std::cout << " 输入对应按键进行操作：" << std::endl;
  std::cout << " 1:输入电话号码进行查询" << std::endl;
  std::cout << " 2:输入用户名称进行查询" << std::endl;
  std::cout << " 3:增加用户电话记录信息" << std::endl;
  std::cout << " 0:退出电话号码查询系统" << std::endl;
  std::cout << "======================" << std::endl;
  return 0;
}

// int insertInfoToFile(std::string filePath,HashTable& table)
// {
//   std::ofstream ofs(filePath, std::ios::app);
//   if (!ofs.is_open())
//   {
//     std::cout << "file open error!" << std::endl;
//     return 1;
//   }

//   std::string info;
//   std::string phoneNumer;
//   info += "PN:";
//   std::cout << "请输入电话号码" << std::endl;
//   std::cin >> phoneNumer;
//   info += phoneNumer;
//   info += "#NM:";
//   std::string userName;
//   std::cout << "请输入用户名" << std::endl;
//   std::cin >> userName;
//   info += userName;
//   info += "#AD:";
//   std::string address;
//   std::cout << "请输入地址信息" << std::endl;
//   std::cin >> address;
//   info += address;
//   ofs << info<<'\n';
//   // ofs.close();
//   return 0;
// }
// template <typename tableType>
// tableType &
// initHashTableByPhoneNumber(std::ifstream &ifs, tableType &hashTable,
//                            std::vector<UserInfo> &user_info_list_phoneNumber) {
//   readUserInfo(ifs, user_info_list_phoneNumber);
//   for (auto atom : user_info_list_phoneNumber) {
//     hashTable[strToInt(atom.getPhoneNumber())] = atom;
//   }
//   return hashTable;
// }
// template <typename tableType>
// tableType &
// initHashTableByUserName(std::ifstream &ifs, tableType &hashTable,
//                         std::vector<UserInfo> &user_info_list_userName) {
//   readUserInfo(ifs, user_info_list_userName);
//   for (auto atom : user_info_list_userName) {
//     hashTable[strToInt(atom.getUserName())] = atom;
//   }
//   return hashTable;
// }
// template <typename tableType, typename InfoType>
// InfoType searchByPhoneNumber(tableType &hashTable, std::string &phoneNumber) {
//   auto index = strToInt(phoneNumber);
//   return hashTable[index];
// }
// template <typename tableType, typename InfoType>
// InfoType searchByUserName(tableType &hashTable, std::string &userName) {
//   auto index = strToInt(userName);
//   return hashTable[index];
// }
// int AppFunction(std::string filePath) {
//   HashTable hashTableByPhoneNumber;
//   HashTable hashTableByUserName;
//   std::vector<UserInfo> user_info_list_phoneNumber;
//   std::vector<UserInfo> user_info_list_userName;
//   std::ifstream ifs_phoneNumber(filePath);
//   std::ifstream ifs_userName(filePath);
//   std::string inputInfo = "";
//   int menuChoose = 0;
//   initHashTableByUserName<>(ifs_phoneNumber, hashTableByUserName,
//                           user_info_list_userName);
//   initHashTableByPhoneNumber(ifs_userName, hashTableByPhoneNumber,
//                              user_info_list_phoneNumber);
//   ifs_phoneNumber.close();
//   ifs_userName.close();
//   menuMsgOut();
//   do {
//     std::cin >> menuChoose;
//     switch (menuChoose) {
//     case 0:
//       std::cout << "正在退出电话号码查询系统..." << std::endl;
//       break;
//     case 1:
//       std::cin >> inputInfo;
//       std::cout << "电话号码:" << inputInfo << " | 查询信息： "
//                 <<
//                 searchByPhoneNumber<HashTable,UserInfo>(hashTableByPhoneNumber,
//                 inputInfo);
//       break;
//     case 2:
//       std::cin >> inputInfo;
//       std::cout << "用户名称:" << inputInfo << " | 查询信息： "
//                 << searchByUserName<HashTable,UserInfo>(hashTableByUserName,
//                 inputInfo);
//       break;
//     default:
//       std::cout << "错误参数请重新输入..." << std::endl;
//     }
//     // if (!menuChoose)
//     //   break;
//     std::cout << "============================" << std::endl;
//   } while (menuChoose);
//   return 0;
// }
// template <typename tableType,typename InfoType>
// int AppFunctionOpen(std::string filePath) {
//   OpenAddressHashTable hashTableByPhoneNumber;
//   OpenAddressHashTable hashTableByUserName;
//   std::vector<UserInfo> user_info_list_phoneNumber;
//   std::vector<UserInfo> user_info_list_userName;
//   std::ifstream ifs_phoneNumber(filePath);
//   std::ifstream ifs_userName(filePath);
//   std::string inputInfo = "";
//   int menuChoose = 0;
//   initHashTableByPhoneNumber<tableType,InfoType>(ifs_phoneNumber,
//   hashTableByPhoneNumber,
//                                         user_info_list_userName);
//   std::cout << "======================" << std::endl;
//   initHashTableByUserName<tableType,InfoType>(ifs_userName,
//   hashTableByUserName,
//                                      user_info_list_phoneNumber);
//   ifs_phoneNumber.close();
//   ifs_userName.close();
//   menuMsgOut();
//   do {
//     std::cin >> menuChoose;
//     switch (menuChoose) {
//     case 0:
//       std::cout << "正在退出电话号码查询系统..." << std::endl;
//       break;
//     case 1:
//       std::cin >> inputInfo;
//       std::cout << "电话号码:" << inputInfo << " | 查询信息： "
//                 <<
//                 searchByPhoneNumber<OpenAddressHashTable,UserInfo>(hashTableByPhoneNumber,
//                 inputInfo);
//       break;
//     case 2:
//       std::cin >> inputInfo;
//       std::cout << "用户名称:" << inputInfo << " | 查询信息： "
//                 <<
//                 searchByUserName<OpenAddressHashTable,UserInfo>(hashTableByUserName,
//                 inputInfo);
//       break;
//     default:
//       std::cout << "错误参数请重新输入..." << std::endl;
//     }
//     // if (!menuChoose)
//     //   break;
//     std::cout << "============================" << std::endl;
//   } while (menuChoose);
//   return 0;
// }
// template <typename tableType> int APP(std::string filePath) {
//   tableType hashTableByPhoneNumber;
//   tableType hashTableByUserName;
//   std::vector<UserInfo> user_info_list_phoneNumber;
//   std::vector<UserInfo> user_info_list_userName;
//   std::ifstream ifs_phoneNumber(filePath);
//   std::ifstream ifs_userName(filePath);
//   std::string inputInfo = "";
//   int menuChoose = 0;
//   initHashTableByPhoneNumber<tableType>(ifs_phoneNumber, hashTableByPhoneNumber,
//                                         user_info_list_userName);
//   std::cout << "======================" << std::endl;
//   initHashTableByUserName<tableType>(ifs_userName, hashTableByUserName,
//                                      user_info_list_phoneNumber);
//   ifs_phoneNumber.close();
//   ifs_userName.close();
//   menuMsgOut();
//   do {
//     std::cin >> menuChoose;
//     switch (menuChoose) {
//     case 0:
//       std::cout << "正在退出电话号码查询系统..." << std::endl;
//       break;
//     case 1:
//       std::cin >> inputInfo;
//       std::cout << "电话号码:" << inputInfo << " | 查询信息： "
//                 << searchByPhoneNumber<tableType>(hashTableByPhoneNumber,
//                                                   inputInfo);
//       break;
//     case 2:
//       std::cin >> inputInfo;
//       std::cout << "用户名称:" << inputInfo << " | 查询信息： "
//                 << searchByUserName<tableType>(hashTableByUserName, inputInfo);
//       break;
//     default:
//       std::cout << "错误参数请重新输入..." << std::endl;
//     }
//     // if (!menuChoose)
//     //   break;
//     std::cout << "============================" << std::endl;
//   } while (menuChoose);
//   return 0;
// }