#ifndef _USER_INFO_
#define _USER_INFO_

#include <fstream>
#include <ostream>
#include <string>
#include <vector>

class UserInfo
{
public:
  UserInfo() = default;
  UserInfo(std::string PhoneNumber, std::string UserName, std::string address) : PhoneNumber(PhoneNumber), UserName(UserName), address(address){};
  std::string getPhoneNumber() const;
  std::string getUserName() const;
  std::string getAddress() const;
  void setPhoneNumber(const std::string &PhoneNumber);
  void setUserName(const std::string &UserName);
  void setAddress(const std::string &address);
  bool isEmpty();
  // friend std::ostream& operator<<(std::ostream &cout,const UserInfo& user_info);
private:
  std::string PhoneNumber;
  std::string UserName;
  std::string address;
};

std::ostream &operator<<(std::ostream &cout, const UserInfo &user_info);

// by fstream to read and write object from user_info.txt
std::string readUserInfo(std::ifstream &ifs, std::vector<UserInfo> &user_infos);
std::string writeUserInfo(std::ofstream &ofs, const UserInfo &userInfo);
std::string writeUserInfos(std::ofstream &ofs, const std::vector<UserInfo> &userInfos);

int strToInt(std::string str);

#endif