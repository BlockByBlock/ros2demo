cmake_minimum_required(VERSION 3.5)
project(example_services)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(say_hello REQUIRED)
find_package(rclcpp REQUIRED)

add_executable(test_service service.cpp)
ament_target_dependencies(test_service rclcpp say_hello)

add_executable(test_client client.cpp)
ament_target_dependencies(test_client rclcpp say_hello)

install(TARGETS 
  test_service
  test_client
  DESTINATION lib/${PROJECT_NAME})

ament_package()
