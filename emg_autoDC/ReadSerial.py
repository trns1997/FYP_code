'''
Graph 1:raw value, DC shift
        filtered value
Graph 2:power
'''
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import random
import datetime as dt
#s = serial.Serial(port='/dev/cu.wchusbserial1420',baudrate=9600)

fig = plt.figure()
ax = fig.add_subplot(2,1,1)
bx = fig.add_subplot(2,1,2)
xs = []
ys = []
zs = []

def animate(i,xs,ys, zs):
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(random.randint(0,20))
    zs.append(random.randint(0,30))
    xs = xs[-20:]
    ys = ys[-20:]
    zs = zs[-20:]

    ax.clear()
    ax.set_ylim(0,100)
    ax.plot(xs,ys,label='raw')
    ax.plot(xs,zs,label='DC shift')
    ax.legend()
    ax.set_title("EMG raw")
    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Time")
    
    
    bx.set_title("EMG Power")
    bx.set_ylabel("Amplitude")
    fig.tight_layout()

    plt.xticks(rotation=45,ha='right')
    #plt.subplots_adjust(bottom=0.3)
    #plt.title("EMG sensor signal")
    #plt.ylabel('random int')

ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, zs), interval=200)
plt.show()

#while (True):
#   print(s.readline())
