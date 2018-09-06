import serial
import time
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft

cnt = 0

ser = serial.Serial('/dev/ttyACM0')
ser.baudrate = 115200

ser.flushInput()

plot_window = 256
y_var = np.array(np.zeros([plot_window]))
y_fft = np.array(np.zeros([(plot_window/2)-1]))

plt.ion()
fig, (ax, ax1) = plt.subplots(2)
line, = ax.plot(y_var)
line_fft, = ax1.plot(y_fft)
ax1.set_ylim(0,10000)

while True:
	ser_bytes = ser.readline()
        decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
#        print(decoded_bytes)
	y_var[cnt%plot_window] = decoded_bytes
	cnt+=1

	if (cnt == plot_window):
		y_fft = fft(y_var)
		#print(y_fft)
		line_fft.set_ydata(np.abs(y_fft[1:plot_window/2]))
		line.set_ydata(y_var)
		ax.relim()
        	ax.autoscale_view()
		fig.canvas.draw()
		fig.canvas.flush_events()
		cnt = 0


