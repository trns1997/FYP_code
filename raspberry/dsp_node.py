#! /usr/bin/env python3

import rospy
from std_msgs.msg import Float32MultiArray

import RPi.GPIO as GPIO
import numpy as np
import time

pub = rospy.Publisher('emg',Float32MultiArray, queue_size=1)
st = None
sf = False
se = False
max_emg = np.zeros(8)
min_emg = np.ones(8)*pow(2,12)-1
#min_emg = np.zeros(4)+999
datum = np.zeros([8,20])
mean_val = np.zeros(8)
pt = 0

def callback(msg):
    global min_emg, max_emg, datum, pt, sf, st, se, mean_val
    if sf == False:
        sf = True
        st = time.time()
        print('Calibrating')
    for i in range(len(max_emg)):
        datum[i,pt] = msg.data[i]
    mean_val = datum.mean(1)
    if pt>=19:
        pt = 0
    else:
        pt = pt+1
        
    if (time.time()-st)<10:
        # Calibrate Mode
        for i in range(len(max_emg)):
            if mean_val[i]>max_emg[i]:
                max_emg[i] = mean_val[i]
            if mean_val[i]<min_emg[i]:
                min_emg[i] = mean_val[i]
    else:
        if se == False:
            se = True
            print('Running')
            print(max_emg)
            print(min_emg)
        #Running Mode
        msg = Float32MultiArray(data=(mean_val-min_emg)*100/(max_emg-min_emg))
        pub.publish(msg)
            
def main():
    global st
    rospy.init_node('dsp_node')
    sub = rospy.Subscriber('emg_ard',Float32MultiArray,callback)
    rospy.spin()
    

if __name__ == '__main__':
    main()

