cmake_minimum_required(VERSION 2.8.3)
project(toad_navigation_global)

find_package(catkin REQUIRED COMPONENTS move_base)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

