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


class print_heading(object):
    
    def __init__(self):

        self.declination = (3.81777/360)*2*pi # Brno (2013)
        
        self.mutex = threading.Lock()
        
        self.heading = []
        
        rospy.Subscriber("/imu_3dm_node/imu/data", Imu, self.imu_callback, queue_size=3)
     
     
    def imu_callback(self,msg):
        
        (roll,pitch,yaw) = euler_from_quaternion([msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w])
        
        if yaw > 0:
            
            yaw = 2*pi - yaw
            
        else:
            
            yaw = -1*yaw
    
        # apply correction for magnetic declination
        yaw += self.declination
    
        if yaw > 2*pi:
        
            yaw -= 2*pi
        
        self.mutex.acquire()
        
        self.heading.append(yaw)
        
        self.mutex.release()   
       
    def spin(self):
        
        
        self.mutex.acquire()
        self.imu_msg = None 
        self.mutex.release()
        
        
        r = rospy.Rate(10)
        
        print "spin"
 
        while not rospy.is_shutdown():
            
            r.sleep()
            
            mean = None
            
            self.mutex.acquire()
            
            if len(self.heading) > 100:
                
                param = norm.fit(self.heading)
                mean = param[0]
                self.heading = []
            
            self.mutex.release()
            
            if mean is None:
                
                continue
        
            
            print "Current heading: " + str(mean) + " (" + str( (mean/(2*pi))*360.0 ) + ")"
 
 
 
def main():
    
    rospy.init_node('heading_node')
    node_class = print_heading()
    try:
        node_class.spin()
    except rospy.ROSInterruptException: pass

if __name__ == '__main__':
    # run main function and exit
    sys.exit(main())