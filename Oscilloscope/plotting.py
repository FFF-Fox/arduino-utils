import serial
import numpy as np
import matplotlib.pyplot as plt
from drawnow import *

# Filter the input string
def filter_stream(data):
    return float(data.decode("utf-8").strip())

# Plotting function for drawnow
def makeFig():
    plt.title("Sensor data")
    plt.ylabel("(C) Degrees Celsius")
    # plt.ylim(-0.2, 5.2)
    plt.plot(tempC, '-')

# Initialize interactive mode
plt.ion()

# Connecting to the serial monitor
port = 'com6'
baud_rate = 9600
arduinoData = serial.Serial(port, baud_rate)

# Array holding the data we need
maxDataPoints = 100
tempC = []

while True:
    while not arduinoData.inWaiting():
        pass

    # Try to take a sensor reading
    try:
        arduinoString = arduinoData.readline()
        C = filter_stream(arduinoString)
        tempC.append(C)
        print(C)
    except:
        pass

    drawnow(makeFig)
    # plt.pause(.001)

    if len(tempC) > maxDataPoints:
        N = len(tempC) - maxDataPoints
        tempC.pop(N)