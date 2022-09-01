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

class ShowImgObj(object):
  def __init__(self):
    #Subscriber
    self.img_sub = rospy.Subscriber('/webcam/image_raw', Image, self.ImgTrans)
    self.img_bridge = CvBridge()

    print("Img Viewer initialized...")

  def ImgTrans(self, data):
    #http://docs.ros.org/en/api/sensor_msgs/html/msg/Image.html
    try:
      cv_img = self.img_bridge.imgmsg_to_cv2(data,desired_encoding='bgr8')
      #print("Converted Img to openCv...")
    except CvBridgeError:
      print(CvBridgeError)
    #Logic goes here
    _GRAY = (50,50,50)
    cv_img_HSV = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
    cv_img_HSV_fil = cv2.inRange(cv_img_HSV,(0,0,0),_GRAY)
    cv_img_HSV_fil = np.stack((cv_img_HSV_fil,)*3, axis=-1)

    img_view = np.concatenate((cv_img, cv_img_HSV_fil), axis=1)
    scale_percent = 75 # percent of original size
    width = int(img_view.shape[1] * scale_percent / 100)
    height = int(img_view.shape[0] * scale_percent / 100)
    dim = (width, height)
  
    # resize image
    resized = cv2.resize(img_view, dim, interpolation = cv2.INTER_AREA)



    
    cv2.imshow('Camera',resized)
    cv2.waitKey(1)



def main():
  rospy.init_node('show_img_node',anonymous=True)
  myImgObj = ShowImgObj()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down...")



if __name__ == '__main__':
  main()