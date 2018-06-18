cmake_minimum_required(VERSION 3.5)
project(call_button_cpp)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rmf_msgs REQUIRED)

file(GLOB WP_FILES ~/WiringNP/wiringPi/*)

include_directories(~/WiringNP/wiringPi)

add_library(wnp_lib ${WP_FILES})

add_executable(call_button_np call_button_np.cpp)
ament_target_dependencies(call_button_np rclcpp rmf_msgs)
target_link_libraries(call_button_np wnp_lib)

install(TARGETS
  call_button_np
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
