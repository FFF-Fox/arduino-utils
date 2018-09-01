import serial
import numpy as np

from pyqtgraph.Qt import QtCore
from plot2D import Plot2D

import argparse

# Argument handling.
parser = argparse.ArgumentParser()
parser.add_argument('-b', '--baud_rate', help='Specify the baud_rate.', type=int)
parser.add_argument('-p', '--port', help='Specify the serial port.', type=str)
parser.add_argument('-m', '--max_data_points', help='Specify the maximum data points.', type=int)

args = parser.parse_args()

if args.port:
    port = args.port
else:
    port = 'com6'

if args.baud_rate:
    baud_rate = args.baud_rate
else:
    baud_rate = 9600

if args.max_data_points:
    max_data_points = args.max_data_points
else:
    max_data_points = 100
    
# Connecting to the serial monitor
arduinoData = serial.Serial(port, baud_rate)

# Parse the input string
def parse_stream(data):
    return float(data.decode("utf-8").strip())

# Array holding the data we need
data = []

plotter = Plot2D()

def update():
    global plotter

    if arduinoData.inWaiting():
        try:
            arduinoString = arduinoData.readline()
            value = parse_stream(arduinoString)
            data.append(value)
        except:
            pass

        plotter.trace(0, range(len(data)), data)

        if len(data) > max_data_points:
            N = len(data) - max_data_points
            data.pop(N)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(20)

plotter.start()