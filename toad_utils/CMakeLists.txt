cmake_minimum_required(VERSION 2.8.3)
project(toad_utils)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  tf
  actionlib_msgs
)

add_action_files(
  DIRECTORY action
  FILES rotate.action
)

generate_messages(
  DEPENDENCIES actionlib_msgs
)

catkin_package(
 CATKIN_DEPENDS geometry_msgs roscpp tf actionlib_msgs
)

include_directories(include)

add_executable(rotate src/rotate.cpp)
target_link_libraries(rotate ${catkin_LIBRARIES})

roslint_cpp()
