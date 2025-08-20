#include <functional>
#include <mutex>
#include <queue>
#include <thread>
#include <vector>
class ThreadPool{

  private:
    std::vector<std::thread> threads;
    std::queue<std::function<void()>> tasks;
    std::mutex mtx;
    int threadSize;
    bool stop;

  public:
    ThreadPool():threadSize(10),stop(false){
      for (auto index=0;index<threadSize;++index) {
        {
          std::lock_guard<std::mutex> lock(mtx);
          while (!tasks.empty()) {
            threads.emplace_back(std::thread(tasks.front()));
            
          }
          
        }
        
      }
    }

};