cmake_minimum_required(VERSION 3.6)

set(lib_name xxtea)
set(target_name ext_${lib_name})

project(${lib_name})

add_library(${target_name} SHARED
  xxtea.c
)

target_include_directories(${target_name} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

set_target_properties(${target_name}
    PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
    FOLDER "External"
    VERSION 1.0
    SOVERSION 1
)

