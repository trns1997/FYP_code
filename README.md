# FYP_code
INTRO

## Getting Started
Once successfully set up the catkin_ws on the RaspberryPi, add the following 2 lines to the Pi's and your PC's `~/.bashrc`.
```
echo 'export export ROS_HOSTNAME=<IP of the Raspberry Pi>' >> ~/.bashrc
```
```
echo 'export export ROS_IP=<IP of the Raspberry Pi>' >> ~/.bashrc
```
```
echo 'export ROS_MASTER_URI=http://<IP of the Raspberry Pi>:11311/' >> ~/.bashrc
```

Make sure the computer and the Pi are connected to the same network. This will allow you to establish connection and visualize data from the Pi on your computer.


## Running the tests
On the Raspberry Pi run the following line:
```
roslaunch <PATH TO catkin_ws>/src/launch/launcher.launch
```
This will run all the nodes and get the running.

On your PC you can now subscribe to the emg node and visualize the data using the following python scripts:
```
./fuse_plot.py
```
The output if everything is setup correctly should look like the following
<img src="https://github.com/trns1997/FYP_code/blob/master/media/fus.gif"/>

```
./get_emg_rasp.py
```

```
./kalman.py
```
The output if everything is setup correctly should look like the following
<img src="https://github.com/trns1997/FYP_code/blob/master/media/kal.gif"/>


## Authors
* **Thomas Narayana Swamy** [trns1997](https://github.com/trns1997)
* **Andre Chan** [andrechanph](https://github.com/andrechanph)

See also the list of [contributors](https://github.com/trns1997/FYP_code/contributors) who participated in this project.

## Acknowledgments
