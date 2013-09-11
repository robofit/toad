#!/usr/bin/env python
###############################################################################
# \file
#
# $Id:$
#
# Copyright (C) Brno University of Technology
#
# This file is part of software developed by dcgm-robotics@FIT group.
# 
# Author: Zdenek Materna (imaterna@fit.vutbr.cz)
# Supervised by: Michal Spanel (spanel@fit.vutbr.cz)
# Date: dd/mm/2012
#
# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
#

import roslib; roslib.load_manifest('toad_utils')
import rospy
import sys


import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def main():
    
    
    rospy.init_node('move_base_test')
    rospy.sleep(1)
    
    move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
    
    if not move_base.wait_for_server(rospy.Duration(10)):
          
          rospy.logerr("move_base not available!")
          return
      
    rospy.loginfo("Starting...")
      
    goal = MoveBaseGoal()
    
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.header.frame_id = "base_footprint" # is this ok???
    
    goal.target_pose.pose.position.x = 3
    goal.target_pose.pose.position.y = 0
    goal.target_pose.pose.position.z = 0
    
    goal.target_pose.pose.orientation.x = 0
    goal.target_pose.pose.orientation.y = 0
    goal.target_pose.pose.orientation.z = 0
    goal.target_pose.pose.orientation.w = 1
    
    rospy.loginfo("Sending goal.")
    move_base.send_goal(goal)
    
    finished_within_time = move_base.wait_for_result(rospy.Duration(5))
    
    if not finished_within_time:
          
          rospy.loginfo("Canceling goal.")
          move_base.cancel_all_goals() 
    
    rospy.loginfo("Finished.")
    
if __name__ == '__main__':
    # run main function and exit
    sys.exit(main())
    
    
    


