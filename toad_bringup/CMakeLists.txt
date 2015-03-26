cmake_minimum_required(VERSION 2.8.3)
project(toad_bringup)

find_package(catkin REQUIRED COMPONENTS p2os_driver p2os_launch robot_pose_ekf microstrain_3dm_gx3_45 stereo_image_proc toad_utils) # p2os_urdf  but_velodyne_proc

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

