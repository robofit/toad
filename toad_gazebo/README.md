toad_gazebo
===========

Simulation of Toad, an outdoor robot.

Requirements:

* standalone version of Gazebo (http://gazebosim.org/wiki/1.6/install#Compiling_From_Source)
* ROS integration packages (http://gazebosim.org/wiki/Tutorials/1.9/Installing_gazebo_ros_Packages)
* hector_gazebo stack (https://github.com/tu-darmstadt-ros-pkg/hector_gazebo)
 * workaround needed!
 * compile stack in rosbuild ws
 * copy libhector_gazebo_ros_imu.so and libhector_gazebo_ros_gps.so to devel/lib in catkin ws


