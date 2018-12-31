#! /usr/bin/env python3

import time

import RPi.GPIO as GPIO


direction = 1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(19,GPIO.OUT, initial=GPIO.HIGH)
print ('dir = HIGH')
GPIO.setup(13,GPIO.OUT)
p = GPIO.PWM(13,800)
p.start(0)
time.sleep(0.5)
print("start")
p.ChangeDutyCycle(100)
try:
    while True:
        raw_input("waiting Press")
        if (direction==1):
            GPIO.output(19,GPIO.LOW)
            time.sleep(0.05)
            direction = 0
            print (GPIO.input(19))
            print ('dir = LOW')
        else:
            GPIO.output(19,GPIO.HIGH)
            time.sleep(0.05)
            direction = 1
            print (GPIO.input(19))
            print ('dir = HIGH')
except KeyboardInterrupt:
    pass
print("end")
p.stop()
GPIO.cleanup()

