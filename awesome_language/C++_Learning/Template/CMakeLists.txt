cmake_minimum_required(VERSION 3.0)
project(template)
aux_source_directory(. DIR_SRCS)
add_executable(template ${DIR_SRCS})