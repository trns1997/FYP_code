#! /usr/bin/env python3

import rospy
from std_msgs.msg import Float32MultiArray

import smbus
import struct

#get respective address from parameter list 
address = 0x0A
bus = smbus.SMBus(1)

def main():
    rospy.init_node('i2c_node')
    pub = rospy.Publisher('emg_ard',Float32MultiArray, queue_size=1)
    rate = rospy.Rate(50)
    while not rospy.is_shutdown():
        try:
            pack = bus.read_i2c_block_data(address,0)
        except Exception:
            print('i2c Missing')
            continue
            #update parameter list
        data = bytes(pack)
        msg = Float32MultiArray(data=list(struct.unpack('4f16x',data)))
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
