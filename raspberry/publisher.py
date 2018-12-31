#! /usr/bin/env python3

import rospy
from rospy.numpy_msg import numpy_msg
from std_msgs.msg import String
from std_msgs.msg import Float32MultiArray, MultiArrayDimension

def talker():
    rospy.init_node('node_publisher')
    #pub = rospy.Publisher('phrases', String, queue_size=10)
    pub = rospy.Publisher('arrays',Float32MultiArray, queue_size=10)

    rate = rospy.Rate(2) #Set publish rate of 2Hz

    #msg_str = String()
    #msg_str = "Hello from the other side"
    msg_float = Float32MultiArray(data=[1.0,2.2,3.3,4.5])
    #msg_float.layout.dim.append(MultiArrayDimension())
    #msg_float.layout.dim[0].size = 4
    #msg_float.layout.dim[0].stride = 1
    #msg_float.data = [1.1,2.2,3.3,4.0,5]

    while not rospy.is_shutdown():
        #pub.publish(msg_str)
        pub.publish(msg_float)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
