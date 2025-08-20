// #include <string>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

namespace KMP {
    auto beNext(string P, vector<int> &next) {
        auto i = 0;
        auto j = -1;
        next[0] = -1;
        while (i < P.length()) {
            if (j == -1 || P[i] == P[j]) {
                ++i;
                ++j;
                next[i] = j;
                } else {
                j = next[j];
            }
        }
}
    auto kmp(string S,string P){
        auto i=0;
        auto j=0;
        vector<int>next(100000);
        beNext(P,next);
        while (i<S.length()&&j<P.length()) {
            if(j==-1||S[i]==P[j]){
                i++;
                j++;
            }else {
                j=next[j];
            }
        }
        return j==P.length()?i-j:-1;
    }

    // void getNext(char *p, int *next) {
    //     next[0] = -1;
    //     int i = 0, j = -1;

    //     while (i < (int)strlen(p)) {
    //         if (j == -1 || p[i] == p[j]) {
    //             ++i;
    //             ++j;
    //             next[i] = j;
    //         } else
    //             j = next[j];
    //     }
    // }

    // int KMP(char *t, char *p) {
    //     int i = 0;
    //     int j = 0;
    //     int next[(int)strlen(p)];
    //     getNext(p,next);
    //     while (i < (int)strlen(t) && j < (int)strlen(p)) {
    //         if (j == -1 || t[i] == p[j]) {
    //             i++;
    //             j++;
    //         } else
    //             j = next[j];
    //     }

    //     if (j == strlen(p))
    //         return i - j;
    //     else
    //         return -1;
    // }
    // int *buildNext(char *P) {        // 构造模式串 P 的 next 表
    //     size_t m = strlen(P), j = 0; // “主”串指针
    //     int *N = new int[m];         // next 表
    //     int t = N[0] = -1;           // 模式串指针
    //     while (j < m - 1)
    //         if (0 > t || P[j] == P[t]) { // 匹配
    //             j++;
    //             t++;
    //             N[j] = t; // 此句可改进为 N[j] = (P[j] != P[t] ? t : N[t]);
    //         } else        // 失配
    //             t = N[t];
    //     return N;
    // }
    // int match(char *P, char *S) {      // KMP 算法
    //     int *next = buildNext(P);      // 构造 next 表
    //     int m = (int)strlen(S), i = 0; // 文本串指针
    //     int n = (int)strlen(P), j = 0; // 模式串指针
    //     while (j < n && i < m)         // 自左向右逐个比对字符
    //         if (0 > j || S[i] == P[j]) // 若匹配，或 P 已移除最左侧
    //         {
    //             i++;
    //             j++;
    //         } // 则转到下一字符
    //         else
    //             j = next[j]; // 模式串右移（注意：文本串不用回退）
    //     delete[] next;       // 释放 next 表
    //     return i - j;
    // }
}
int main(){
    string S="abcdabc";
    string P="bcd";
    cout<<KMP::kmp(S, P)<<endl;
    // char *s = new char[8]; // 分配足够的内存来存储 "Hello, World!"
    // strcpy(s, "abcdabc");   // 将字符串复制到分配的内存中
    // char *p = new char[6]; // 分配足够的内存来存储 "Hello, World!"
    // strcpy(p, "cdac"); // 将字符串复制到分配的内存中
 
    // auto  *s="abcde";
    // char  *p={'c','d','z'};
    // cout<<KMP::KMP(s,p)<<endl;
    // cout<<KMP::match(s,p)<<endl;
    
    // cout<<KMP::KMP(s,p)<<endl;
}