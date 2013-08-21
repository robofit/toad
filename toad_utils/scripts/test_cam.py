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

import roslib; roslib.load_manifest('toad_utils')
import rospy

from sensor_msgs.msg import Image

import threading

class print_timestamp():
  
  def __init__(self):
      
      
      rospy.Subscriber("/stereo/left/image_rect_color", Image, self.img_callback, queue_size=5)
      
      self.last_ts = None
      
      
      
  def img_callback(self,msg):
        
      print msg.header.stamp.to_sec()
      
      if self.last_ts is None:
      
        self.last_ts = msg.header.stamp
        return
        
        
      if self.last_ts.to_sec() > msg.header.stamp.to_sec():
      
        print "ouch!"
        
      self.last_ts = msg.header.stamp

 
def main():
 
  ts = print_timestamp()
  rospy.spin()
      
if __name__ == '__main__':

    rospy.init_node('test_cam')
    rospy.sleep(2)
    
    try:

        main()
        
    except rospy.ROSInterruptException:
        print "program interrupted before completion"

