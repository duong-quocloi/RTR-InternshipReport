#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from mavros_msgs.msg import OverrideRCIn
from mavros_msgs.srv import CommandLong, CommandBool, SetMode

from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

from time import sleep
from pymavlink import mavutil

'''
RC stuff: https://discuss.bluerobotics.com/t/rc-override-not-working-with-sitl-ardusub-mavros/12046/8
https://github.com/mavlink/mavros/issues/1632
https://discuss.bluerobotics.com/t/simulating-manual-control-using-mavros/1745/71?page=4
'''

_MAV_CMD_DO_SET_MODE = 176
_MAV_CMD_COMPONENT_ARM_DISARM = 400

_ROLL = 0
_PITCH = 1
_YAW = 3
_THROTTLE = 2

the_connection = mavutil.mavlink_connection('udpin:localhost:14551')
the_connection.wait_heartbeat() 
print("Heartbeat from system (system %u component %u)" %
      (the_connection.target_system, the_connection.target_component))

class ImgObj(object):
  def __init__(self):
    #Service
    self.send_command_long = rospy.ServiceProxy('/mavros/cmd/command', CommandLong)
    self.arm = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
    self.set_mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
    #Publisher
    self.rc_override_pub = rospy.Publisher("mavros/rc/override", OverrideRCIn, queue_size=10)
    self.rc_msg_override = OverrideRCIn()
    #Subscriber
    self.img_sub = rospy.Subscriber('/webcam/image_raw', Image, self.ImgTrans)
    self.img_bridge = CvBridge()
    
    print("Setting to guided mode...")
    self.set_mode(custom_mode='GUIDED')
    print("Arm the quad")
    self.arm(True)
    sleep(3)
    print("Take off...")
    self.send_command_long(False,22,10,0,0,0,0,0,0,5)
    print("Object initialized...")
  def ImgTrans(self, data):
    #http://docs.ros.org/en/api/sensor_msgs/html/msg/Image.html
    try:
      cv_img = self.img_bridge.imgmsg_to_cv2(data,desired_encoding='bgr8')
      print("Converted Img to openCv...")
      # cv2.imshow('Camera',cv_img)
      # cv2.waitKey()
    except CvBridgeError:
      print(CvBridgeError)
      self.set_mode(custom_mode='LAND')
    #Logic goes here
    _GRAY = (30,30,30)
    cv_img_HSV = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
    cv_img_HSV_fil = cv2.inRange(cv_img_HSV,(0,0,0),_GRAY)
    has_road = np.any(cv_img_HSV_fil) 

    #Logic end here
    print(has_road)
    if(has_road): self.rc_msg_override.channels[_PITCH] = 1600
    else: self.rc_msg_override.channels[_PITCH] = 1500
    self.rc_override_pub.publish(self.rc_msg_override)
    print("Command sent!")




def main():
  myImgObj = ImgObj()
  rospy.init_node('get_img_node',anonymous=True)

  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down...")



if __name__ == '__main__':
  main()