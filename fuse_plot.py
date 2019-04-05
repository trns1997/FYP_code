#! /usr/bin/env python

import rospy
from std_msgs.msg import Float32MultiArray
import multiprocessing as mp
import struct
from threading import Thread

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import serial
from matplotlib.lines import Line2D
import numpy as np

##############################################################################
#
# Processing Class
# ================
#
# This class plots data it receives from a pipe.
#
exit_flag = False

def terminate():
    plt.close('all')


class ProcessPlotter(object):
    def __init__(self):
        self.x = [0]
        self.y = [[0] for i in range(2)]
        print(self.y)

    def call_back(self):
        while self.pipe.poll():
            data = self.pipe.recv()
            if data is None:
                terminate()
                return False
            else:
                if len(data) == 3:
                    self.x.append(data[0])
                    self.x = self.x[-1000:]
                    for i in range(len(self.y)):
                        self.y[i].append(data[1 + i])
                        self.y[i] = self.y[i][-1000:]
        return True

    def animate(self, frame):
        # self.ax.clear()
        # self.ax.plot(self.x,self.y)
        # self.fig.canvas.draw()
        self.graphs[0].set_xlim(self.x[0], self.x[-1])
        self.graphs[0].figure.canvas.draw()

        for i in range(len(self.y)):
            self.lines[i].set_data(self.x, self.y[i])

        # self.bx.set_xlim(self.x[0],self.x[-1])
        # self.bx.figure.canvas.draw()
        return self.lines

    def __call__(self, pipe):
        print('starting plotter...')

        self.pipe = pipe
        self.fig, self.graphs = plt.subplots(2, 1, sharex=True)

        self.lines = [Line2D(self.x, self.y[0], color='b', label="FUS_ELBOW"),
                      Line2D(self.x, self.y[1], color='r', label="FUS_SHOULDER")]

        for i in range(2):
            self.graphs[i].add_line(self.lines[0 + i * 1])
            self.graphs[i].set_ylim(-255, 255)
            self.graphs[i].set_title("Output")
            self.graphs[i].set_ylabel("Amplitude")
            self.graphs[i].set_xlabel("Time")
            self.graphs[i].legend()

        # self.graphs[2].add_line(self.lines[0])
        # self.graphs[2].add_line(self.lines[1])
        # # self.graphs[2].add_line(self.lines[2])
        # # self.graphs[2].add_line(self.lines[3])
        # self.graphs[2].set_ylim(0, 255)
        # self.graphs[2].legend()
        # self.graphs[2].set_title("Filtered Output")
        # self.graphs[2].set_ylabel("Amplitude")
        # self.graphs[2].set_xlabel("Time")

        self.fig.tight_layout()
        timer = self.fig.canvas.new_timer(interval=1)
        timer.add_callback(self.call_back)
        timer.start()
        ani = animation.FuncAnimation(self.fig, self.animate, interval=1, blit=True)
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
            target=self.plotter, args=(plotter_pipe,))
        self.plot_process.daemon = True
        self.plot_process.start()

    def plot(self, data=None):
        send = self.plot_pipe.send
        if data is not None:
            data = [self.count] + list(data)
        # print(str(data[3]) + "," + str(data[6]))
        send(data)
        self.count += 1


def callback(msg):
    data_x = [msg.data[0] - msg.data[1], msg.data[2] - msg.data[3]]
    # print(data_x)
    pl.plot(data_x)


def main():
    global pl
    pl = NBPlot()
    rospy.init_node('plotter_node')
    sub = rospy.Subscriber('fuse', Float32MultiArray, callback)
    rospy.spin()


if __name__ == '__main__':
    main()
