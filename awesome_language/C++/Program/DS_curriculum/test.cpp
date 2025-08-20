#include <fstream>
#include <iostream>
#include <vector>
#include <string>

using namespace std;

int test()
{
  string line;
  ifstream ifs("user_info.txt");
  while (getline(ifs, line))
  {
    cout << line << endl;
    auto index_PN = line.find("PN:");
    auto index_NM = line.find("NM:");
    auto index_AD = line.find("AD:");
    cout << line.substr(index_PN + 3, 11) << endl;
    cout << line.substr(index_NM + 3, index_AD - index_NM - 4) << endl;
    cout << line.substr(index_AD + 3, 100) << endl;
  }

  cout << line.find(":") << endl;
  return 0;
}