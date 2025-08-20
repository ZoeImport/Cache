#include "UserInfo.h"
#include <cctype>
#include <ostream>
#include <string>
#include <unordered_set>
#include <vector>

std::string UserInfo::getPhoneNumber() const { return this->PhoneNumber; }
void UserInfo::setPhoneNumber(const std::string &PhoneNumber)
{
  this->PhoneNumber = PhoneNumber;
}
std::string UserInfo::getUserName() const { return this->UserName; }
void UserInfo::setUserName(const std::string &UserName)
{
  this->UserName = UserName;
}
std::string UserInfo::getAddress() const { return this->address; }
void UserInfo::setAddress(const std::string &address)
{
  this->address = address;
}

std::string readUserInfo(std::ifstream &ifs,
                         std::vector<UserInfo> &user_infos)
{
  std::string line;
  if (!ifs.is_open())
  {
    return "file can not be opened !!!";
  }
  while (std::getline(ifs, line))
  {
    auto index_PN = line.find("PN:");
    auto index_NM = line.find("NM:");
    auto index_AD = line.find("AD:");
    user_infos.emplace_back(
        UserInfo(line.substr(index_PN + 3, 11),
                 line.substr(index_NM + 3, index_AD - index_NM - 4),
                 line.substr(index_AD + 3, 100)));
  }
  ifs.close();
  return user_infos.empty() ? "there is no user info in the txt file"
                            : " read info successfully !!!";
}

std::ostream &operator<<(std::ostream &cout, const UserInfo &user_info)
{
  cout << "PhoneNumber: " << user_info.getPhoneNumber()
       << "|UserName: " << user_info.getUserName()
       << "|Address: " << user_info.getAddress() << std::endl;
  return cout;
}

bool UserInfo::isEmpty()
{
  return this->getPhoneNumber() == "" && this->getUserName() == "" && this->getAddress() == "";
}

int strToInt(std::string str)
{
  int uniqueInteger = 0;
  std::unordered_set<char> uniqueChars;
  for (char ch : str)
  {
    // 判断字符是否已经出现过
    if (uniqueChars.find(ch) == uniqueChars.end())
    {
      // 字符第一次出现，将其ASCII值累加
      uniqueInteger += static_cast<int>(ch);
      uniqueChars.insert(ch);
    }
  }
  return uniqueInteger;
}