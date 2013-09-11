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
import actionlib
from toad_utils.msg import rotateAction, rotateGoal



def main():
    
  rospy.init_node('test_rotate')
 
  client = actionlib.SimpleActionClient('rotate',rotateAction)
  
  rospy.loginfo("Waiting for server...")
  client.wait_for_server()
  
  rospy.loginfo('Sending goal...')
  goal = rotateGoal()
  
  goal.requested_yaw = -0.7
  
  client.send_goal(goal)
  client.wait_for_result()
  result = client.get_result()
  
  
  rospy.loginfo("Finished.")
  
  
if __name__ == '__main__':

  try:
      main()
  except rospy.ROSInterruptException: pass
