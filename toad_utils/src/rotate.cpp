#include "toad_utils/rotate.h"


using namespace toad_utils;

RobotDriver::RobotDriver(ros::NodeHandle &nh, std::string name)
  {

	as_.reset( new actionserver(nh, name, boost::bind(&RobotDriver::executeCB, this, _1), false) );

	action_name_ = name;

    nh_ = nh;
    //set up the publisher for the cmd_vel topic
    cmd_vel_pub_ = nh_.advertise<geometry_msgs::Twist>("cmd_vel", 3);

    as_->start();

    ROS_INFO("Started.");

  }

RobotDriver::~RobotDriver() {



}

bool RobotDriver::GetCurrentOrientation(tf::Quaternion& quat) {

  geometry_msgs::PoseStamped pose;

  pose.header.frame_id = "base_link";
  pose.header.stamp = ros::Time(0);

  pose.pose.position.x = 0;
  pose.pose.position.y = 0;
  pose.pose.position.z = 0;

  pose.pose.orientation.x = 0;
  pose.pose.orientation.y = 0;
  pose.pose.orientation.z = 0;
  pose.pose.orientation.w = 1;

  try {

	  listener_.transformPose("odom",pose,pose);

  } catch (tf::TransformException& ex){

	  ROS_ERROR("%s",ex.what());
      return false;

    }

  quat.setX(pose.pose.orientation.x);
  quat.setY(pose.pose.orientation.y);
  quat.setZ(pose.pose.orientation.z);
  quat.setW(pose.pose.orientation.w);

  return true;

}

void RobotDriver::executeCB(const rotateGoalConstPtr &goal)
 {


   ROS_INFO("%s: Received goal.", action_name_.c_str());

   bool ret = true;
   bool ret2 = false;

   bool dir = goal->requested_yaw > 0;

   double ang = fabs(goal->requested_yaw);

   while(ang > 2*M_PI)
   	{
   		ang -= 2*M_PI;
   	}

   double th = 0.9*M_PI;

   if (ang > th) {

	   ret = turnOdom(dir, th);

   }

   ret2 = turnOdom(dir, fabs(ang - th));


   if(ret && ret2)
   {
	// result_.sequence = feedback_.sequence;
	 ROS_INFO("%s: Succeeded to rotate robot.", action_name_.c_str());
	 // set the action state to succeeded
	 as_->setSucceeded();

   } else {

	   ROS_INFO("%s: Failed to rotate robot.", action_name_.c_str());
	   as_->setAborted();

   }


 }



bool RobotDriver::turnOdom(bool clockwise, double radians)
{


	tf::Quaternion start_orientation;
	tf::Quaternion current_orientation;

	if (!GetCurrentOrientation(start_orientation)) {

		ROS_ERROR("Can't get start orientation.");

	}

	double max_velocity = 0.25;
	double min_velocity = 0.075;

	//we will be sending commands of type "twist"
	geometry_msgs::Twist base_cmd;
	//the command will be to turn at 0.25 rad/s
	base_cmd.linear.x = base_cmd.linear.y = 0.0;
	base_cmd.angular.z = 0.0;

	tf::Quaternion start_inv = start_orientation.inverse();

	ros::Time time_start = ros::Time::now();
	ros::Duration timeout = ros::Duration(45);

	ros::Rate rate(10.0);
	bool done = false;
	while (!done && nh_.ok())
	{

		if (ros::Time::now()-time_start > timeout) {

			ROS_ERROR("Hmm, tried to rotate robot for too much time...");
			break;

		}

		if (!GetCurrentOrientation(current_orientation)) {

				ROS_ERROR("Can't get current orientation.");
				rate.sleep();
				continue;

			}

		double angle = fabs(tf::getYaw(current_orientation * start_inv));


		std::cout << angle << " " << radians << std::endl;

		double vel = max_velocity;

		// TODO code something more clever
		if (angle > 0.9*radians) {

			vel = min_velocity;

		}


		  if (angle >= radians)
		  {

			  base_cmd.angular.z = 0;
			  cmd_vel_pub_.publish(base_cmd);
			  cmd_vel_pub_.publish(base_cmd);
			  cmd_vel_pub_.publish(base_cmd);

			  done = true;
		  }
		  else
		  {

			base_cmd.angular.z = vel;
			if (clockwise) base_cmd.angular.z = -base_cmd.angular.z;

			cmd_vel_pub_.publish(base_cmd);
			rate.sleep();
		  }

	} // while

	if (done) return true;
	return false;

}



int main(int argc, char** argv)
{
  ros::init(argc, argv, "rotate_robot");

  ros::NodeHandle nh;
  RobotDriver driver(nh,"rotate");

  ros::spin();

  return 0;
}
