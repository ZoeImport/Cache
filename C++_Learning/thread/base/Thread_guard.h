#include <thread>


//RAII
//保证线程一定能在结束前就运行
class Thread_guard {

  std::thread &t;

public:
  Thread_guard(std::thread &_t) : t(_t) {}
  ~Thread_guard() {
    if (t.joinable()) {
      t.join();
    }
  }
  Thread_guard(const Thread_guard &) = delete; // 删除拷贝构造函数
  Thread_guard &operator=(const Thread_guard &) = delete; // 删除拷贝赋值运算函数
};