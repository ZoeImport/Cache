#include <ios>
#include <iostream>
#include <fstream>
#include <istream>
#include <iterator>
#include <string>
using namespace std;
struct Person{
    string name;
    int age;
};
int main(){
    
    //read
    ifstream ifs;
    char buf[1024]={0};
    
    ifs.open("/home/zoe/Learning/Notes/C++_NewBegin/fileStream/read.txt",
             ios::in);
    while (ifs.getline(buf, sizeof(buf))) {
      cout << buf << endl;
    }
    ifs.close();
    
    // write
        ofstream ofs;
    ofs.open("/home/zoe/Learning/Notes/C++_NewBegin/fileStream/info.txt",
             ios::out);
    ofs << "this is first line info for txt" << endl;
    ofs << "this is second line info for txt" << endl;
    ofs.close();

    //write as binary
    Person person={"Lucy",18};
    ofs.open("/home/zoe/Learning/Notes/C++_NewBegin/fileStream/binaryWrite.txt",ios::out|ios::binary);
    ofs.write((const char *)&person,sizeof(Person));
    ofs.close();
    // read and writ
    Person p;
    ifs.open("/home/zoe/Learning/Notes/C++_NewBegin/fileStream/binaryWrite.txt",ios::in|ios::binary);
    if(ifs.is_open()){
      ifs.read((char *)&p, sizeof(Person));
      cout << p.name << endl;
    }else{
        cout<<"open file failure";
    }
    ifs.close();
    //文件的打开方式：
    /*
    ios::in     read
    ios::out    write
    ios::ate    begin with the end of file
    ios::app    append to end of file
    ios::trunc  delete file if file exist
    ios::binary open file as binary
    
    Ps:can use more than one way to open file by |,such as ios::in|ios::out
    */
}