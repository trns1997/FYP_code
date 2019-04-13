from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
#QtGui.QApplication.setGraphicsSystem('raster')

import rospy
import struct
from std_msgs.msg import Float32MultiArray


app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Basic plotting examples")
win.setWindowTitle('Example PlotWidget')
win.resize(800,800)
pg.setConfigOptions(antialias=True)
#mw = QtGui.QMainWindow()
#mw.resize(800,800)

p6 = win.addPlot(title='Elbow')

curve = pg.PlotCurveItem(pen='y')
curve2= pg.PlotCurveItem(pen='b')
p6.addItem(curve)
p6.addItem(curve2)
data = np.random.normal(size=(10,1000))
data2= np.random.normal(size=(10,1000))

ptr = 0
def update6():
    global curve, data, ptr, p6, curve2, data2
    curve.setData(data[ptr%10])
    curve2.setData(data2[ptr%10])
    if ptr == 0:
        p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
    ptr += 1

win.nextRow()

p7 = win.addPlot(title='Shoulder')

curve7 = pg.PlotCurveItem(pen='r')
curve72= pg.PlotCurveItem(pen='b')
p7.addItem(curve7)
p7.addItem(curve72)
data7 = np.random.normal(size=(10,1000))
data72= np.random.normal(size=(10,1000))

ptr7 = 0
def update7(msg):
    global curve7, data7, ptr7, p7, curve72, data72
    global curve, data, ptr, p6, curve2, data2
    curve7.setData(data7[ptr7%10])
    curve72.setData(data72[ptr7%10])
    if ptr7 == 0:
        p7.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
    ptr7 += 1

    curve.setData(data[ptr%10])
    curve2.setData(data2[ptr%10])
    if ptr == 0:
        p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
    ptr += 1  

#timer = QtCore.QTimer()
#timer.timeout.connect(update7)
#timer.start(50)  

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        print("IN")
        rospy.init_node('plotter_node')
        sub = rospy.Subscriber('emg',Float32MultiArray, update7)
        rospy.spin()
