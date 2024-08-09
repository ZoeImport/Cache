#include <iostream>
#include <map>
#include <string>

using namespace std;

bool canConstruct(string ransomNote, string magazine) {
  map<char, int> mp_note;
  map<char, int> mp_mg;
  for (auto &ch : ransomNote) {
    if (mp_note.count(ch)) {
      ++mp_note[ch];
    }else {
      mp_note[ch]=1;
    }
  }
  for (auto &ch :magazine) {
    if (mp_mg.count(ch)) {
      ++mp_mg[ch];
    }else {
      mp_mg[ch]=1;
    }
  }
  for (auto &kv : mp_note) {
    auto temp=kv.first;
    if (mp_note[temp]>mp_mg[temp]||mp_mg.find(temp)==mp_mg.end()) {
      return false;
    }
  }
  return true;
}


class Solution {
public:
    bool canConstruct(string ransomNote, string magazine) {
        int record[26]={0};
        for(int i=0;i<ransomNote.size();i++){
            record[ransomNote[i]-'a']++;
        }
        for(int i=0;i<magazine.size();i++){
            record[magazine[i]-'a']--;
        }
        for(int i=0;i<26;i++){
            if(record[i]>0){
                return false;
            }
        }
        return true;

    }
};

int main() { cout << canConstruct(string("aa"), string("aab")) << endl; }