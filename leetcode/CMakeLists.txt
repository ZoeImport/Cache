cmake_minimum_required(VERSION 3.0)
project(lCode)
file(GLOB CPP_FILES "*.cpp")
foreach(CPP_FILE ${CPP_FILES})
    get_filename_component(EXE_NAME ${CPP_FILE} NAME_WE)
    add_executable(${EXE_NAME} ${CPP_FILE})
    target_compile_options(${EXE_NAME} PRIVATE -g)    
endforeach()
    
