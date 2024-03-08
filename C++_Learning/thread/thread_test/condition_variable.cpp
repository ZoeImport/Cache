#include <chrono>
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <thread>

std::mutex mtx;
std::condition_variable cv;
std::queue<int> queue;

void producer(){
  for (auto count=1;count<=10; ++count) {
    {
      std::lock_guard<std::mutex>lgProducer(mtx);
      queue.push(count);
      std::cout<<count<<" was produced by producer func"<<std::endl;
    }
      cv.notify_one();
      std::this_thread::sleep_for(std::chrono::milliseconds(1000));
  }
}

void comsumer(){
  while (1) {
    std::unique_lock<std::mutex>lgConsumer(mtx);
    cv.wait(lgConsumer,[]{return !queue.empty();});
    auto count=queue.front();
    queue.pop();
    std::cout<<count<<" was comsumed by comsumer"<<std::endl;
  }
}
int main(){
  std::thread producer_t(producer);
  std::thread comsumer_t(comsumer);
  producer_t.join();
  comsumer_t.join();
}