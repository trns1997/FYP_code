"""
Serial in: A1 Raw, DC Shift, Power, A2 Raw, DC Shift, Power

Matplotlib in background process
        

"""

import multiprocessing as mp
import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D
import numpy as np
import random
import datetime

import serial
import struct
###############################################################################
#
# Processing Class
# ================
#
# This class plots data it receives from a pipe.
#

class ProcessPlotter(object):
    def __init__(self):
        self.x = [0]
        self.y = [[0] for i in range(6)]
        print(self.y)

    def terminate(self):
        plt.close('all')

    def call_back(self):
        while self.pipe.poll():
            data = self.pipe.recv()
            if data is None:
                self.terminate()
                return False
            else:
                if (len(data)==7):
                    self.x.append(data[0])
                    self.x = self.x[-1000:]
                    for i in range(len(self.y)):
                        self.y[i].append(data[1+i])
                        self.y[i] = self.y[i][-1000:]
        return True

    def animate(self, frame):
        #self.ax.clear()
        #self.ax.plot(self.x,self.y)
        #self.fig.canvas.draw()
        self.graphs[0].set_xlim(self.x[0],self.x[-1])
        self.graphs[0].figure.canvas.draw()

        for i in range(len(self.y)):
            self.lines[i].set_data(self.x,self.y[i])

        #self.bx.set_xlim(self.x[0],self.x[-1])
        #self.bx.figure.canvas.draw()
        return self.lines

    def __call__(self, pipe):
        print('starting plotter...')

        self.pipe = pipe
        self.fig, self.graphs = plt.subplots(3,1,sharex=True)
        
        self.lines = [Line2D(self.x,self.y[0],color='b',label="A1 raw"),
                      Line2D(self.x,self.y[1],color='g',label="DC Shift"),
                      Line2D(self.x,self.y[2],color='c',label="A1"),
                      Line2D(self.x,self.y[3],color='b',label="A2 raw"),
                      Line2D(self.x,self.y[4],color='g',label="DC Shift"),
                      Line2D(self.x,self.y[5],color='r',label="A2")]

        for i in range(2):
            self.graphs[i].add_line(self.lines[0+i*3])
            self.graphs[i].add_line(self.lines[1+i*3])
            self.graphs[i].set_ylim(0,700)
            self.graphs[i].set_title("EMG Value")
            self.graphs[i].set_ylabel("Amplitude")
            self.graphs[i].set_xlabel("Time")
            self.graphs[i].legend()

        self.graphs[2].add_line(self.lines[2])
        self.graphs[2].add_line(self.lines[5])
        self.graphs[2].set_ylim(0,100)
        self.graphs[2].legend()
        self.graphs[2].set_title("Filtered Output")
        self.graphs[2].set_ylabel("Amplitude")
        self.graphs[2].set_xlabel("Time")

        self.fig.tight_layout()
        timer = self.fig.canvas.new_timer(interval=2)
        timer.add_callback(self.call_back)
        timer.start()
        ani = animation.FuncAnimation(self.fig,self.animate, interval=2, blit=True)
        print('...done')

        plt.show()

###############################################################################
#
# Plotting class
# ==============
#
# This class uses multiprocessing to spawn a process to run code from the
# class above. When initialized, it creates a pipe and an instance of
# ``ProcessPlotter`` which will be run in a separate process.
#
# When run from the command line, the parent process sends data to the spawned
# process which is then plotted via the callback function specified in
# ``ProcessPlotter:__call__``.
#


class NBPlot(object):
    
    def __init__(self):
        self.count = 0
        self.plot_pipe, plotter_pipe = mp.Pipe()
        self.plotter = ProcessPlotter()
        self.plot_process = mp.Process(
            target=self.plotter, args=(plotter_pipe,), daemon=True)
        self.plot_process.start()

    def plot(self, data=None):
        send = self.plot_pipe.send
        if (data!=None):
            data=[self.count]+list(data)
        print(data)
        send(data)
        self.count+=1


def main():
    s = serial.Serial(port='/dev/cu.wchusbserial1420',baudrate=115200)
    pl = NBPlot()
    #for ii in range(10):
    #    data = [ii,random.randint(0,10)]
    #    pl.plot(data)
    #    time.sleep(0.2)
    while True:
        datum = s.read(24)
        data = struct.unpack("iIfiIf",datum)
        pl.plot(data)
        


if __name__ == '__main__':
    if plt.get_backend() == "MacOSX":
        mp.set_start_method("forkserver")
    main()
