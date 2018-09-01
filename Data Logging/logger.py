import serial
import time
import datetime
import argparse

# Argument handling.
parser = argparse.ArgumentParser()
parser.add_argument('-b', '--baud_rate', help='Specify the baud_rate.', type=int)
parser.add_argument('-p', '--port', help='Specify the serial port.', type=str)
parser.add_argument('-f', '--filename', help='Specify the file to save the data.', type=str)
parser.add_argument('-s', '--save_data', help='Save the data.', action="store_true")
parser.add_argument('-t', '--timestamp', help='Add timestamp to the data.', action="store_true")
args = parser.parse_args()

if args.port:
    port = args.port
else:
    port = 'com6'

if args.baud_rate:
    baud_rate = args.baud_rate
else:
    baud_rate = 9600

if args.timestamp:
    use_timestamp = True
else:
    use_timestamp = False

if args.filename:
    filename = args.filename
else:
    filename = 'datalog.csv'

if args.save_data:
    save_data = True
else:
    save_data = False
    
def parse_serial(data):
    """ Parse the serial data into a string. """
    data = data.strip()
    data = data.decode("utf-8")

    return data

def timestamp_data(data):
    """ Append a timestamp as a string in a list of data.
        Input data: list. """
    timestamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    data.append(timestamp)

    return data

def save(data):
    """ Appends the data in the specified file as csv.
        Input data: list. """
    with open(filename, 'a') as f:
        line = ','.join(data) + '\n'
        f.write(line)

def default_process(data):
    """ Reads a string with comma separated values and logs it appropriately.
        Input data: a csv string. """
    data = data.split(',')

    if use_timestamp:
        data = timestamp_data(data)
    if save_data:
        save(data)

    print('\t'.join(data))

def read_serial(serial_connection, process=None):
    """ Read data from a serial connection and process them. If a process is not
        specified, then the default_process(...) function is used. The process function should
        take a string as input (the data read from the connection). """
    while True:
        try:
            while not serial_connection.inWaiting():
                pass

            # Parse the serial data.
            serial_data = serial_connection.readline()
            data_string = parse_serial(serial_data)

            # Process the data.
            if process is None:
                default_process(data_string)
            else:
                process(data_string)      

        # Exit the loop on Ctrl + C.
        except KeyboardInterrupt:
            break

def dht_example(data_string):
    """ An example process that can be used with the data_sampling.ino sketch to demonstrate the
        use of a process(...) function in read_serial(...).
        Use: 
            arduino_serial = serial.Serial(port, baud_rate)

            read_serial(arduino_serial, dht_example)
            
            arduino_serial.close()
            print("Bye..")
    """
    # data is a csv line, so we split it in a list.
    data = data_string.split(',')
    # Add a timestamp to the data using timestamp_data(...).
    data = timestamp_data(data)

    # Use the save_data argument, along with the save(...) function
    # to append the data in a csv file.
    if save_data:
        save(data)

    # Format the data in a readable way and print them to console.
    out = '{}\tHumidity: {} %\tTemperature: {} C'.format(data[-1], data[0], data[1])
    print(out)

if __name__=="__main__":
    """ Works as a data logger. Reads from the serial port a csv line of data and prints
        them in the console. There are arguments to specify whether to timestamp the data
        or/and save them to a file. """
    arduino_serial = serial.Serial(port, baud_rate)

    read_serial(arduino_serial)

    arduino_serial.close()
    print("Bye..")