# min required version for cmake
cmake_minimum_required(VERSION 3.0)
# name for project
project(dataStructure)
# get full filename for extensions is cpp
file(GLOB CPP_FILES "*.cpp")
# do a range for every cppFile
foreach(CPP_FILE ${CPP_FILES})
    # extract fileName 
    get_filename_component(EXE_NAME ${CPP_FILE} NAME_WE)
    # add exeFile for every cppFile
    add_executable(${EXE_NAME} ${CPP_FILE})
    # create the last targetFile named as fileName
    target_compile_options(${EXE_NAME} PRIVATE -g)    
endforeach()
    
