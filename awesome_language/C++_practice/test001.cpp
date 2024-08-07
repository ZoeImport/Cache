#include <array>
#include <cstddef>
#include <iostream>

 template <typename T, std::size_t N> // 关于
constexpr std::size_t arraySize(T (&)[N]) noexcept // constexpr
{                                                  // 和noexcept
  return N;                                        // 的信息
}

template<typename E>
constexpr std::size_t arraySize(E && arr){
    return arr.size();
}

int main(){
    std::array<int,10> arr1;
    int arr2[20];
    std::cout<<arraySize(arr1)<<std::endl;
    std::cout<<arraySize(arr2)<<std::endl;
}