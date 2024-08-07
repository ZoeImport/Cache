#include <deque>
#include <iostream>
#include <string>
#include <vector>

using namespace std;
namespace overloadMid {
    class Person{
        public:
            Person()=default;
            Person(std::string name,int age):name(name),age(age){};
            auto operator[](const std::string& name);
        private:
            std::string name;
            int age;
    };
    auto Person::operator[](const std::string &name){
        return ;
    }
}



int main() {
            int n;
            cin >> n;

            vector<int> a(n);
            for (int i = 0; i < n; i++) {
              cin >> a[i];
            }

            int k;
            cin >> k;

            deque<int> window; // 双端队列，用于维护窗口中的值

            for (int i = 0; i < n; i++) {
              // 处理窗口中的过期元素
              while (!window.empty() && window.front() < i - k) {
                window.pop_front();
              }

              // 输出当前窗口最小值
              cout << a[window.front()] << " ";

              // 添加当前元素到窗口，保持窗口中的元素按升序排列
              while (!window.empty() && a[i] < a[window.back()]) {
                window.pop_back();
              }
              window.push_back(i);
            }

            return 0;
}