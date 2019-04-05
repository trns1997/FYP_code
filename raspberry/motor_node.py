#! /usr/bin/env python3

'''
GPIO Pin:
-----------------------------------
| GPIO 6  | Elbow Dir    |
-----------------------------------
| GPIO 19 | Elbow PWM    |
-----------------------------------
| GPIO 16 | Shoulder PWM |
-----------------------------------
| GPIO 20 | Shoulder Dir |
-----------------------------------
'''
import rospy
from std_msgs.msg import Float32MultiArray

import RPi.GPIO as GPIO
import numpy as np

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(6,GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(20,GPIO.OUT, initial=GPIO.HIGH)

GPIO.setup(22,GPIO.OUT, initial=GPIO.HIGH)

GPIO.setup(19,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
p = GPIO.PWM(19,800)
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
        
    if (abs(np.mean(avg_arr)) > 8):
        p.ChangeDutyCycle(abs(np.mean(avg_arr)))
    else:
        p.ChangeDutyCycle(0)
        
    if (np.mean(avg_arr2)>0):
        GPIO.output(20,GPIO.LOW)
    else:
        GPIO.output(20,GPIO.HIGH)
        
    if (abs(np.mean(avg_arr2)) > 8):
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
