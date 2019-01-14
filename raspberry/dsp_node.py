#! /usr/bin/env python3

import rospy
from std_msgs.msg import Float32MultiArray

import RPi.GPIO as GPIO
import numpy as np
import time

pub = rospy.Publisher('emg',Float32MultiArray, queue_size=1)
st = None
sf = False
max_emg = np.zeros(4)
#min_emg = np.zeros(4)+999
datum = np.zeros([4,20])
pt = 0

def callback(msg):
    global max_emg, datum, pt, sf, st
    if sf == False:
        sf = True
        st = time.time()
    if (time.time()-st)<10:
        print('Calibrating')
        # Calibrate Mode
        for i in range(len(max_emg)):
            if msg.data[i]>max_emg[i]:
                max_emg[i] = msg.data[i]
    else:
        #print('Running')
        #Running Mode
        for i in range(len(max_emg)):
            datum[i,pt] = msg.data[i]*100/max_emg[i]
        if pt>=19:
            pt = 0
        else:
            pt = pt+1
        msg = Float32MultiArray(data=datum.mean(1))
        pub.publish(msg)
            
def main():
    global st
    rospy.init_node('dsp_node')
    sub = rospy.Subscriber('emg_ard',Float32MultiArray,callback)
    rospy.spin()
    

if __name__ == '__main__':
    main()

