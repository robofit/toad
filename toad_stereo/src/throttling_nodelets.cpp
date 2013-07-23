#include <pluginlib/class_list_macros.h>
#include <sensor_msgs/CompressedImage.h>
#include <dynamic_reconfigure/ConfigDescription.h>
#include <dynamic_reconfigure/Config.h>
#include <sensor_msgs/CameraInfo.h>
#include <sensor_msgs/Image.h>

#include <nodelet_topic_tools/nodelet_throttle.h>
namespace camera_throttle_nodelets{
typedef nodelet_topic_tools::NodeletThrottle<sensor_msgs::CompressedImage> NodeletThrottleCompressedImage;
//typedef nodelet_topic_tools::NodeletThrottle<dynamic_reconfigure::ConfigDescription> NodeletThrottleParameterDescription;
//typedef nodelet_topic_tools::NodeletThrottle<dynamic_reconfigure::Config> NodeletThrottleParameterUpdates;
//typedef nodelet_topic_tools::NodeletThrottle<sensor_msgs::CameraInfo> NodeletThrottleCameraInfo;
typedef nodelet_topic_tools::NodeletThrottle<sensor_msgs::Image> NodeletThrottleImage;
}

PLUGINLIB_EXPORT_CLASS(toad_stereo::NodeletThrottleCompressedImage, nodelet::Nodelet);
//PLUGINLIB_EXPORT_CLASS(toad_stereo::NodeletThrottleParameterDescription, nodelet::Nodelet);
//PLUGINLIB_EXPORT_CLASS(toad_stereo::NodeletThrottleParameterUpdates, nodelet::Nodelet);
PLUGINLIB_EXPORT_CLASS(toad_stereo::NodeletThrottleImage, nodelet::Nodelet);
//PLUGINLIB_EXPORT_CLASS(toad_stereo::NodeletThrottleCameraInfo, nodelet::Nodelet);
