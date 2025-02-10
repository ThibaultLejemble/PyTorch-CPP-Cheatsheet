cmake_minimum_required(VERSION 3.10)
project(PyTorch_CPP_Cheatsheet)

find_package(Torch REQUIRED)

add_executable(pytorch_cpp_cheatsheet pytorch_cpp_cheatsheet.cpp)
target_link_libraries(pytorch_cpp_cheatsheet "${TORCH_LIBRARIES}")
set_property(TARGET pytorch_cpp_cheatsheet PROPERTY CXX_STANDARD 17)