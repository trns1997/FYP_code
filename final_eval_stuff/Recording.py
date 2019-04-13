#! /usr/bin/env python

import rospy
from std_msgs.msg import Float32MultiArray

f = None

def callback(msg):
    f.write(str(msg.data[0])+"\t"+str(msg.data[1])+"\n")

def shutdown():
    f.write("\r\n")
    f.close()
    print("FILE save")
            
    
if __name__ == "__main__":
    rospy.init_node('recording_node')
    f = open("./recording.txt","a+")
    rospy.on_shutdown(shutdown)
    sub = rospy.Subscriber('emg',Float32MultiArray,callback)
    print("REcording Started")
    rospy.spin()
