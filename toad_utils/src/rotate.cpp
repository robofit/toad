#include "toad_utils/rotate.h"


using namespace toad_utils;

RobotDriver::RobotDriver(ros::NodeHandle &nh, std::string name)
  {


	//rotateActionGoalConstPtr goal;
	//executeCB(goal);

	as_.reset( new actionserver(nh, name, boost::bind(&RobotDriver::executeCB, this, _1), false) );

	action_name_ = name;

    nh_ = nh;
    //set up the publisher for the cmd_vel topic
    cmd_vel_pub_ = nh_.advertise<geometry_msgs::Twist>("cmd_vel", 1);

    as_->start();

  }

RobotDriver::~RobotDriver() {



}

tf::StampedTransform RobotDriver::GetCurrentTransform() {

  listener_.waitForTransform("odom", "base_footprint",
						   ros::Time(0), ros::Duration(10.0));

  tf::StampedTransform current_transform;
  listener_.lookupTransform("odom", "base_footprint",
						  ros::Time(0), current_transform);
  return current_transform;
}

void RobotDriver::executeCB(const rotateGoalConstPtr &goal)
 {

   // helper variables
   ros::Rate r(1);
   bool success = true;
   double rot_step = 0.05;

   bool promenna = 0;
   while(promenna == 0)
   {
std::cout << "Rotuji smerem k cili" << std::endl;
	   if (goal->requested_yaw > 0)
   promenna = turnOdom(0,rot_step);
	   else
   promenna = turnOdom(1,rot_step);
   }

   if(success)
   {
	// result_.sequence = feedback_.sequence;
	 ROS_INFO("%s: Succeeded", action_name_.c_str());
	 // set the action state to succeeded
	 as_->setSucceeded();
   }
 }



bool RobotDriver::turnOdom(bool clockwise, double radians)
{

	while(radians < 0)
	{
		radians += 2*M_PI;
	}
	while(radians > 2*M_PI)
	{
		radians -= 2*M_PI;
	}
	//wait for the listener to get the first message
	listener_.waitForTransform("base_footprint", "odom",
							   ros::Time(0), ros::Duration(1.0));

	//we will record transforms here
	tf::StampedTransform start_transform;
	tf::StampedTransform current_transform;

	//record the starting transform from the odometry to the base frame
	listener_.lookupTransform("base_footprint", "odom",
							  ros::Time(0), start_transform);

	//we will be sending commands of type "twist"
	geometry_msgs::Twist base_cmd;
	//the command will be to turn at 0.25 rad/s
	base_cmd.linear.x = base_cmd.linear.y = 0.0;
	base_cmd.angular.z = 0.25;
	if (clockwise) base_cmd.angular.z = -base_cmd.angular.z;

	//the axis we want to be rotating by
	tf::Vector3 desired_turn_axis(0,0,1);
	if (!clockwise) desired_turn_axis = -desired_turn_axis;

	ros::Rate rate(10.0);
	bool done = false;
	while (!done && nh_.ok())
	{

		  //get the current transform
		  try
		  {
			listener_.lookupTransform("base_footprint", "odom",
									  ros::Time(0), current_transform);
		  }
		  catch (tf::TransformException& ex)
		  {
			ROS_ERROR("%s",ex.what());
			break;
		  }

		  tf::Transform relative_transform = start_transform.inverse() * current_transform;
		  tf::Vector3 actual_turn_axis = relative_transform.getRotation().getAxis();
		  double angle_turned = relative_transform.getRotation().getAngle();


		  if ( actual_turn_axis.dot( desired_turn_axis ) < 0 )
			angle_turned = 2 * M_PI - angle_turned;


		  if (angle_turned >= radians)
		  {
			done = true;
		  }
		  else
		  {
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
