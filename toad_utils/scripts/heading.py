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
import threading
from math import pi
import sys
import numpy as np
from scipy.stats import norm

from sensor_msgs.msg import Imu

from tf.transformations import euler_from_quaternion

#from std_msgs.msg import Float32
from toad_utils.msg import heading as HeadingMsg


class print_heading(object):
    
    def __init__(self):
    
        self.buff_len = rospy.get_param("~filter_len", 0)

        self.declination = rospy.get_param("~declination", (3.81777/360)*2*pi) # Brno (2013)
        
        self.mutex = threading.Lock()
        
        self.heading = []
        
        rospy.Subscriber("/imu_3dm_node/imu/data", Imu, self.imu_callback, queue_size=3)
        self.pub = rospy.Publisher('/robot_heading', HeadingMsg)
        
        rospy.loginfo("Heading script. Declination: " + str(round(self.declination,2)) + ", filter len: " + str(round(self.buff_len)) )
        
        self.published = False
     
     
    def imu_callback(self,msg):
        
        (roll,pitch,yaw) = euler_from_quaternion([msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w])
        
        #yaw += pi/2.0 # why????????
    
        yaw *= -1.0 
    
        # apply correction for magnetic declination
        yaw += self.declination
    
        #if yaw >= 2*pi:
        
        #    yaw -= 2*pi
            
        #elif yaw < 0:
            
        #    yaw += 2*pi
        
        #print str(yaw/(2*pi)*360)
        
        if len(self.heading) > 0 and len(self.heading) >= self.buff_len:
            
            self.heading.pop(0)
        
        self.heading.append(yaw)
        
        mmsg = HeadingMsg()
        
        if self.buff_len > 1:
        
            param = norm.fit(self.heading)
                
            mmsg.mean = param[0]
            mmsg.stddev = param[1]
            
        else:
            
            mmsg.mean = yaw
            mmsg.stddev = 0.0
        
        self.pub.publish(mmsg)
        
        if self.published is False:
            
            rospy.loginfo("Publishing robot heading.")
            self.published = True
       
 
def main():
    
    rospy.init_node('heading_node')
    node_class = print_heading()
    try:
        rospy.spin()
    except rospy.ROSInterruptException: pass

if __name__ == '__main__':
    # run main function and exit
    sys.exit(main())
