#! /usr/bin/env python3

import rospy
from std_msgs.msg import Float32MultiArray

import RPi.GPIO as GPIO
import numpy as np

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(19,GPIO.OUT, initial=GPIO.HIGH)
print ('dir = HIGH')
GPIO.setup(13,GPIO.OUT)
p = GPIO.PWM(13,800)
p.start(0)
avg_arr = np.zeros(20)
i = 0

def callback(msg):
    global i, avg_arr
    avg_arr[i] = msg.data[0]-msg.data[1]
    #print(msg.data[0]-msg.data[1])
    if (np.mean(avg_arr)<0):
        GPIO.output(19,GPIO.LOW)
    else:
        GPIO.output(19,GPIO.HIGH)       
    if (abs(np.mean(avg_arr)) > 2):
        p.ChangeDutyCycle(100)
    else:
        p.ChangeDutyCycle(0)
    i+=1
    if i>=20:
        i = 0
    

def main():
    rospy.init_node('motor_node')
    sub = rospy.Subscriber('emg',Float32MultiArray,callback)
    rospy.spin()
    

if __name__ == '__main__':
    main()
