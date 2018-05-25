cmake_minimum_required(VERSION 3.5)
project(wc_demo)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

file(GLOB SERIAL_SOURCE libserial/*)

include_directories(
    libserial	
)

add_library(lib_serial
	${SERIAL_SOURCE}
)

add_executable(wc wc_one.cpp)
ament_target_dependencies(wc rclcpp std_msgs geometry_msgs)

add_executable(test_wc test_wc.cpp)
ament_target_dependencies(test_wc rclcpp std_msgs)

add_executable(led roslit.cpp)
target_link_libraries(led lib_serial)
ament_target_dependencies(led rclcpp std_msgs lib_serial)

install(TARGETS
  wc
  test_wc
  led
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
