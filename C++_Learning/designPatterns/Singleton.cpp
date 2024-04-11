#include <atomic>
#include <iostream>
#include <mutex>

class HungerSingleto {
public:
  HungerSingleto(const HungerSingleto &) = delete;
  HungerSingleto &operator=(const HungerSingleto) = delete;
  static HungerSingleto *getInstance() { return singleton; }
  void toString() { std::cout << "this is a hungerSingleton" << std::endl; }

private:
  HungerSingleto() = default;
  static HungerSingleto *singleton;
};
// instancing
HungerSingleto *HungerSingleto::singleton = new HungerSingleto;

class LazySingleton {
public:
  LazySingleton(const LazySingleton &) = delete;
  LazySingleton &operator=(const LazySingleton) = delete;
  static LazySingleton *getInstance() {
    if (lazySingleton == nullptr) {
      // instancing
      lazySingleton = new LazySingleton;
    }
    return lazySingleton;
  }
  void toString() { std::cout << "this is a lazySingleton" << std::endl; }

private:
  LazySingleton() = default;
  static LazySingleton *lazySingleton;
};

LazySingleton *LazySingleton::lazySingleton = nullptr;

class ThreadSafeSingleton {
public:
  ThreadSafeSingleton(const ThreadSafeSingleton &) = delete;
  ThreadSafeSingleton &operator=(const ThreadSafeSingleton) = delete;
  static ThreadSafeSingleton *getInstance() {
    if (threadSingleton == nullptr) {
      mtx.lock();
      if (threadSingleton == nullptr) {
        // instancing
        threadSingleton = new ThreadSafeSingleton;
      }
      mtx.unlock();
    }
    return threadSingleton;
  }
  void toString() { std::cout << "this is a threadSingleton" << std::endl; }

private:
  ThreadSafeSingleton() = default;
  static ThreadSafeSingleton *threadSingleton;
  static std::mutex mtx;
};

ThreadSafeSingleton *ThreadSafeSingleton::threadSingleton = nullptr;
std::mutex ThreadSafeSingleton::mtx;

class AtomicSingleton {
public:
  AtomicSingleton(const AtomicSingleton &) = delete;
  AtomicSingleton &operator=(const AtomicSingleton) = delete;
  static AtomicSingleton *getInstance() {
    auto temp = atomicSingleton.load();
    if (temp == nullptr) {
      mtx.lock();
      if (temp == nullptr) {
        // instancing
        temp = new AtomicSingleton;
        atomicSingleton.store(temp);
      }
      mtx.unlock();
    }
    return temp;
  }
  void toString() { std::cout << "this is a atomicSingleton" << std::endl; }

private:
  AtomicSingleton() = default;
  static std::atomic<AtomicSingleton *> atomicSingleton;
  static std::mutex mtx;
};

std::atomic<AtomicSingleton *> AtomicSingleton::atomicSingleton;
std::mutex AtomicSingleton::mtx;

class LocalStaticSingleton {
public:
  LocalStaticSingleton(const LocalStaticSingleton &) = delete;
  LocalStaticSingleton &operator=(const LocalStaticSingleton) = delete;
  static LocalStaticSingleton *getInstance() {
    static LocalStaticSingleton localStaticSingleton;
    return &localStaticSingleton;
  }
  void toString() { std::cout << "this is a localStaticSingleton" << std::endl; }

private:
  LocalStaticSingleton() = default;
};

int main() {
  auto hunger = HungerSingleto::getInstance();
  hunger->toString();
  auto lazy = LazySingleton::getInstance();
  lazy->toString();
  auto threadSingleton = ThreadSafeSingleton::getInstance();
  threadSingleton->toString();
  auto atomic = AtomicSingleton::getInstance();
  atomic->toString();
  auto localStatic = LocalStaticSingleton::getInstance();
  localStatic->toString();

}
