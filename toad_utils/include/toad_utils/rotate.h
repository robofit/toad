#ifndef ROT_NODE_H_
#define ROT_NODE_H_

#include <ros/ros.h>
#include <actionlib/server/simple_action_server.h>
#include <toad_utils/rotateAction.h>

#include <geometry_msgs/Pose.h>
#include <geometry_msgs/Pose2D.h>
#include <tf/transform_listener.h>

#include <tf/tf.h>
#include <geometry_msgs/Twist.h>


namespace toad_utils {

typedef actionlib::SimpleActionServer<rotateAction> actionserver;

class RobotDriver
{
private:

  //! The node handle we'll be using
  ros::NodeHandle nh_;
  //! We will be publishing to the "cmd_vel" topic to issue commands
  ros::Publisher cmd_vel_pub_;
  //! We will be listening to TF transforms as well
  tf::TransformListener listener_;

  boost::shared_ptr<actionserver> as_;

  std::string action_name_;

public:

   //! ROS node initialization
   RobotDriver(ros::NodeHandle &nh, std::string name);
   ~RobotDriver();

   bool GetCurrentOrientation(tf::Quaternion& quat);

   void executeCB(const rotateGoalConstPtr &goal);

   bool turnOdom(bool clockwise, double radians);


};



} // ns


#endif /* NODE_H_ */
