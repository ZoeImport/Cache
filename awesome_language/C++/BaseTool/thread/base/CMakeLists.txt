cmake_minimum_required(VERSION 3.0)
project(thread)
aux_source_directory(. DIR_SRCS)
add_executable(thread ${DIR_SRCS})