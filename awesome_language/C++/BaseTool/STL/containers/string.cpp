//string
/*
    创建和初始化：
        std::string str;：创建一个空字符串。
        std::string str("Hello, World!");：创建并初始化一个字符串。
        std::string str = "Hello, World!";：同样是创建并初始化字符串的一种方式。
        std::string str(5, 'A');：创建一个包含5个字符 'A' 的字符串。

    访问字符串内容：
        str[i]：访问字符串中的第 i 个字符。
        str.at(i)：安全访问字符串中的第 i 个字符，会抛出异常如果索引越界。
        str.front()：访问字符串的第一个字符。
        str.back()：访问字符串的最后一个字符。
        str.c_str()：返回一个以 null 结尾的 C 风格字符串表示。

    修改字符串内容：
        str.append(" text");：在字符串末尾追加文本。
        str += " more text";：与 append 类似，用于字符串连接。
        str.insert(position, "inserted");：在指定位置插入文本。
        str.erase(position, count)：从指定位置删除指定数量的字符。
        str.replace(start, count, newStr)：替换指定范围的字符为新的字符串。
        str.pop_back()：删除字符串的最后一个字符。
        str.clear()：清空字符串。

    获取字符串信息：
        str.length() 或 str.size()：返回字符串的长度（字符数量）。
        str.empty()：检查字符串是否为空。
        str.find("substring")：查找子字符串的位置，返回第一个匹配的位置。
        str.rfind("substring")：从字符串末尾查找子字符串的位置，返回最后一个匹配的位置。
        str.substr(start, length)：提取从指定位置开始指定长度的子字符串。

    比较字符串：
        str.compare("other")：比较字符串与另一个字符串。
        str == "other"：检查字符串是否与另一个字符串相等。

    转换：
        std::to_string(value)：将数值转换为字符串。
        std::stoi(str)：将字符串转换为整数。

*/
#include<iostream>
#include<string>
#include<algorithm>

using namespace std;

int main(){
    string str1="hello world";
    cout<<str1.append(" text").erase(0,5)<<endl;
}
