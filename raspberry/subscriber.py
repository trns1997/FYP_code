#! /usr/bin/env python3

import rospy
from std_msgs.msg import String

def callback(data):
    print (data.data)

def listener():
    rospy.init_node('node_subscriber')
    #sub = rospy.Subscriber('/phrases', String,callback)
    sub = rospy.Subscriber('emg',Float32MultiArray,callback)
    rospy.spin()    #create a loop that will keep program in excution

if __name__ == '__main__':
    listener()
