#!/usr/bin/env python
import rospy
from control_node import *

from sensor_msgs.msg import Image
from mavros_msgs.srv import CommandLong, CommandBool, SetMode
from std_msgs.msg import Bool

from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

from time import sleep

class ImgObj(object):
  def __init__(self):
    #Service
    self.send_command_long = rospy.ServiceProxy('/mavros/cmd/command', CommandLong)
    self.arm = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
    self.set_mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)

    #Subscriber
    self.img_sub = rospy.Subscriber('/webcam/image_raw', Image, self.ImgTrans)
    self.img_bridge = CvBridge()

    #Publisher
    self.signal_pub = rospy.Publisher('img_signal',Bool,queue_size=10)
    
    #Init variable
    self.img_signal = Bool()

    print("Img Object initialized...")

  def ImgTrans(self, data):
    #http://docs.ros.org/en/api/sensor_msgs/html/msg/Image.html
    try:
      cv_img = self.img_bridge.imgmsg_to_cv2(data,desired_encoding='bgr8')
      #print("Converted Img to openCv...")
      # cv2.imshow('Camera',cv_img)
      # cv2.waitKey()
    except CvBridgeError:
      print(CvBridgeError)
      self.set_mode(custom_mode='LAND')
    #Logic goes here
    _GRAY = (50,50,50)
    cv_img_HSV = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
    cv_img_HSV_fil = cv2.inRange(cv_img_HSV,(0,0,0),_GRAY)
    has_road = np.count_nonzero(cv_img_HSV_fil==0) < int(640*480*85/100)


    #Logic end here
    self.img_signal.data = has_road
    self.signal_pub.publish(self.img_signal)
    
    #print("Command sent!")




def main():
  rospy.init_node('get_img_node',anonymous=True)
  myImgObj = ImgObj()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down...")



if __name__ == '__main__':
  main()