cmake_minimum_required(VERSION 3.28)
project(test)

# set()
add_executable(test test.cpp)
target_link_libraries(test LOG)