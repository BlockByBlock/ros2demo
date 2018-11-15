
cmake_minimum_required(VERSION 2.8.3)

project(pathplanner)

find_package(catkin REQUIRED COMPONENTS
  actionlib
  move_base_msgs
  rospy
)

catkin_package(
  CATKIN_DEPENDS actionlib move_base_msgs rospy 
)
