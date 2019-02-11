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

###############################################################################
#
# Processing Class
# ================
#
# This class plots data it receives from a pipe.
#
exit_flag = False

init = False

def terminate():
    plt.close('all')

class ProcessPlotter(object):
    def __init__(self):
        self.x = [0]
        self.y = [[0] for i in range(12)]
        print(self.y)

    def call_back(self):
        while self.pipe.poll():
            data = self.pipe.recv()
            if data is None:
                terminate()
                return False
            else:
                if len(data) == 13:
                    self.x.append(data[0])
                    self.x = self.x[-500:]
                    for i in range(len(self.y)):
                        self.y[i].append(data[1 + i])
                        self.y[i] = self.y[i][-500:]
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

        self.lines = [Line2D(self.x, self.y[0], color='b', label="A1"),
                      Line2D(self.x, self.y[1], color='g', label="F1"),
                      Line2D(self.x, self.y[2], color='r', label="FIN1"),
                      Line2D(self.x, self.y[3], color='c', label="A2"),
                      Line2D(self.x, self.y[4], color='m', label="F2"),
                      Line2D(self.x, self.y[5], color='y', label="FIN2"),
                      Line2D(self.x, self.y[6], color='b', label="A3"),
                      Line2D(self.x, self.y[7], color='g', label="F3"),
                      Line2D(self.x, self.y[8], color='r', label="FIN3"),
                      Line2D(self.x, self.y[9], color='c', label="A4"),
                      Line2D(self.x, self.y[10], color='m', label="F4"),
                      Line2D(self.x, self.y[11], color='y', label="FIN5")]

        for i in range(2):
            self.graphs[i].add_line(self.lines[0 + i * 6])
            self.graphs[i].add_line(self.lines[1 + i * 6])
            self.graphs[i].add_line(self.lines[2 + i * 6])
            self.graphs[i].add_line(self.lines[3 + i * 6])
            self.graphs[i].add_line(self.lines[4 + i * 6])
            self.graphs[i].add_line(self.lines[5 + i * 6])
            self.graphs[i].set_ylim(0, 100)
            self.graphs[i].set_title("EMG Value")
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
        timer = self.fig.canvas.new_timer(interval=20)
        timer.add_callback(self.call_back)
        timer.start()
        ani = animation.FuncAnimation(self.fig, self.animate, interval=20, blit=True)
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
        # print(str(data))
        send(data)
        self.count += 1


def callback(msg):
    global init, A, P, I, R1, R2, C, R, Q, x_hat, z, G
    if not init:
        A  = 1
        P = [1, 1, 1, 1]
        I = 1
        R1 = 0.70
        R2 = 0.50
        # C = np.array([[1],
        #              [1]])
        # R = np.array([[R1, 0], 
        #             [0, R2]])
        C = 1
        R = R1*R2
        Q = 0.005
        G = [0, 0, 0, 0]
        z = [0, 0, 0, 0]
        x_hat = [0, 0, 0, 0]
        init = True
        
        # z = np.array([[msg.data[2]],
        #           [msg.data[3]]])
        # P = A * P * A + Q
        # print(P)
        # G = np.matmul(P * C.transpose(), np.linalg.inv(np.matmul((C * P), C.transpose()) + R))
        # print(G)
        # P = (I - np.matmul(G,C)) * P
        # print(P)
        # x_hat = x_hat + np.matmul(G, (z - C * x_hat))
        # print(x_hat)
        

    # z = np.array([[msg.data[2]],
    #               [msg.data[3]]])
    # x_hat = A * x_hat
    # P = A * P * A + Q

    # G = np.matmul(P * C.transpose(), np.linalg.inv(np.matmul((C * P), C.transpose()) + R))
    # P = (I - np.matmul(G,C)) * P
    # x_hat = x_hat + np.matmul(G, (z - C * x_hat))

    z[0] = (msg.data[0]*msg.data[4]*100)/6000
    z[1] = (msg.data[1]*msg.data[5]*100)/6000
    z[2] = (msg.data[2]*msg.data[6]*100)/6000
    z[3] = (msg.data[3]*msg.data[7]*100)/6000

    # x_hat = A * x_hat
    # P = A * P * A + Q

    # G = (P*C)/(C*P*C + R)
    # P = (I - G*C)*P
    # x_hat = x_hat + G*(z - C * x_hat)

    for i in range(4):
        x_hat[i] = A * x_hat[i]
        P[i] = A * P[i] * A + Q
        G[i] = (P[i]*C)/(C*P[i]*C + R)
        P[i] = (I - G[i]*C)*P[i]
        x_hat[i] = x_hat[i] + G[i]*(z[i] - C * x_hat[i])

    data_x = [msg.data[0], msg.data[4], x_hat[0], msg.data[1], msg.data[5], x_hat[1], msg.data[2], msg.data[6], x_hat[2], msg.data[3], msg.data[7], x_hat[3]]
    # print(data_x)
    pl.plot(data_x)


def main():
    global pl
    pl = NBPlot()
    rospy.init_node('plotter_node')
    sub = rospy.Subscriber('emg', Float32MultiArray, callback)
    rospy.spin()


if __name__ == '__main__':
    main()
