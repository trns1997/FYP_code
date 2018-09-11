import serial
import time
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft

cnt = 0

ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 115200

ser.flushInput()

plot_window = 512

y_var_bi = np.array(np.zeros([plot_window]))
y_fft_bi = np.array(np.zeros([(plot_window/2)-1]))

y_var_tri = np.array(np.zeros([plot_window]))
y_fft_tri = np.array(np.zeros([(plot_window/2)-1]))

plt.ion()
fig, (ax, ax1) = plt.subplots(2)
line_bi, = ax.plot(y_var_bi)
line_tri, = ax.plot(y_var_tri)
line_fft_bi, = ax1.plot(y_fft_bi)
line_fft_tri, = ax1.plot(y_fft_tri)
ax1.set_ylim(0,5000)

while True:
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
		#print(y_fft_bi)
		line_fft_bi.set_ydata(np.abs(y_fft_bi[1:plot_window/2]))
		line_bi.set_ydata(y_var_bi)
		line_fft_tri.set_ydata(np.abs(y_fft_tri[1:plot_window/2]))
		line_tri.set_ydata(y_var_tri)
		ax.relim()
        	ax.autoscale_view()
		fig.canvas.draw()
		fig.canvas.flush_events()
		cnt = 0
