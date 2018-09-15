#!/usr/bin/env python
# license removed for brevity
import rospy
import serial
import time
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from std_msgs.msg import Float64

cnt = 0

ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 115200

ser.flushInput()

plot_window = 512

y_var_bi = np.array(np.zeros([plot_window]))
y_fft_bi = np.array(np.zeros([(plot_window/2)-1]))
power_bi = np.array(np.zeros([plot_window]));

y_var_tri = np.array(np.zeros([plot_window]))
y_fft_tri = np.array(np.zeros([(plot_window/2)-1]))
power_tri = np.array(np.zeros([plot_window]));

diff = np.array(np.zeros([plot_window]));

plt.ion()
fig, (ax, ax1, ax2, ax3) = plt.subplots(4)
line_bi, = ax.plot(y_var_bi)
line_tri, = ax.plot(y_var_tri)
line_fft_bi, = ax1.plot(y_fft_bi)
line_fft_tri, = ax1.plot(y_fft_tri)
line_power_bi, = ax2.plot(power_bi)
line_power_tri, = ax2.plot(power_tri)
line_diff, = ax3.plot(diff)
ax1.set_ylim(0,5000)
ax2.set_ylim(0,500000)
ax3.set_ylim(-500000,500000)

pub = rospy.Publisher('/rrbot/joint2_position_controller/command', Float64, queue_size=10)
rospy.init_node('vel_controller', anonymous=True)

while not rospy.is_shutdown():
	ser_bytes = ser.readline()
	ser_list = ser_bytes.splitlines()[0].split(",")
#	print(ser_list)
        decoded_bytes_bi = float(ser_list[0].decode("utf-8"))
        decoded_bytes_tri = float(ser_list[1].decode("utf-8"))
#       print(decoded_bytes)
	y_var_bi[cnt%plot_window] = decoded_bytes_bi
	y_var_tri[cnt%plot_window] = decoded_bytes_tri
	cnt+=1

	if (cnt == plot_window):
		y_fft_bi = fft(y_var_bi)
		y_fft_tri = fft(y_var_tri)

		power_bi = (sum((np.abs(y_fft_bi[1:plot_window/2]))**2)/((plot_window/2)-1))*np.array(np.ones([plot_window]))
		power_tri = (sum((np.abs(y_fft_tri[1:plot_window/2]))**2)/((plot_window/2)-1))*np.array(np.ones([plot_window]))

		diff = power_bi - power_tri

		line_fft_bi.set_ydata(np.abs(y_fft_bi[1:plot_window/2]))
		line_bi.set_ydata(y_var_bi)
		line_power_bi.set_ydata(power_bi)

		line_fft_tri.set_ydata(np.abs(y_fft_tri[1:plot_window/2]))
		line_tri.set_ydata(y_var_tri)
		line_power_tri.set_ydata(power_tri)

		line_diff.set_ydata(diff)

		ax.relim()
        	ax.autoscale_view()
		fig.canvas.draw()
		pub.publish(Float64(diff[0]/100000))
		fig.canvas.flush_events()
		cnt = 0
