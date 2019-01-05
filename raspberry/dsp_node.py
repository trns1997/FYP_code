#! /usr/bin/env python3

import rospy
from std_msgs.msg import Float32MultiArray

import RPi.GPIO as GPIO
import numpy as np

def callback(msg):

    

def main():
    rospy.init_node('dsp_node')
    sub = rospy.Subscriber('emg',Float32MultiArray,callback)
    rospy.spin()
    

if __name__ == '__main__':
    main()

