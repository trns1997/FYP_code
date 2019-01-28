#! /usr/bin/env python3

'''
GPIO Pin:
-----------------------------------
| GPIO 6  | Pin 31 | Elbow Dir    |
-----------------------------------
| GPIO 13 | Pin 33 | Elbow PWM    |
-----------------------------------
| GPIO 16 | Pin 36 | Shoulder PWM |
-----------------------------------
| GPIO 26 | Pin 37 | Shoulder Dir |
-----------------------------------
'''
import rospy
from std_msgs.msg import Float32MultiArray

import RPi.GPIO as GPIO
import numpy as np

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(6,GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(26,GPIO.OUT, initial=GPIO.HIGH)

GPIO.setup(13,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
p = GPIO.PWM(13,800)
p2= GPIO.PWM(16,800)
p.start(0)
p2.start(0)
avg_arr = np.zeros(20)
avg_arr2= np.zeros(20)
i = 0

def callback(msg):
    global i, avg_arr
    avg_arr[i] = msg.data[0]-msg.data[1]
    avg_arr2[i]= msg.data[2]-msg.data[3]
    
    if (np.mean(avg_arr)>0):
        GPIO.output(6,GPIO.LOW)
    else:
        GPIO.output(6,GPIO.HIGH)       
    if (abs(np.mean(avg_arr)) > 20):
        p.ChangeDutyCycle(100)
    else:
        p.ChangeDutyCycle(0)

    if (np.mean(avg_arr2)>0):
        GPIO.output(26,GPIO.LOW)
    else:
        GPIO.output(26,GPIO.HIGH)       
    if (abs(np.mean(avg_arr2)) > 20):
        p2.ChangeDutyCycle(100)
    else:
        p2.ChangeDutyCycle(0)

    i+=1
    if i>=20:
        i = 0
    

def main():
    rospy.init_node('motor_node')
    sub = rospy.Subscriber('emg',Float32MultiArray,callback)
    rospy.spin()
    

if __name__ == '__main__':
    main()
