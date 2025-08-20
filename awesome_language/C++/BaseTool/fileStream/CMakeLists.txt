cmake_minimum_required(VERSION 3.0)
project(fileStream)
aux_source_directory(. DIR_SRCS)
add_executable(fileStream ${DIR_SRCS})