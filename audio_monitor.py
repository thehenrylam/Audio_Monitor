"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""
from sys import byteorder

import struct
import numpy as np
import matplotlib.pyplot as plt

import pyaudio
import threading
import time

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100

idi = None
odi = None

data_int = np.zeros(2*CHUNK)

exit_flag = False

def convertDataToArray(data):
    data_int = np.frombuffer(data, dtype=np.int16)
    if byteorder == 'big':
        data_int = data_int.byteswap()
    return data_int

def selectIO(p):
    global idi, odi
    
    # Print out device's IO information to the user
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        print("{}\t : {}/{}".format(
            device_info['index'],
            device_info['name'],
            device_info['defaultSampleRate']
            ))
    # Have the user select the program's input
    idi = input("What input device should be used? (default: {})\n".format(p.get_default_input_device_info()['index']))
    if (idi == ""):
        idi = p.get_default_input_device_info()
    else:
        idi = int(idi)
    # Have the user select the program's output
    odi = input("What output device should be used? (default: {})\n".format(p.get_default_output_device_info()['index']))
    if (odi == ""):
        odi = p.get_default_output_device_info()
    else:
        odi = int(odi)
    
    return

def main():
    global idi, odi
    
    p = pyaudio.PyAudio()

    selectIO(p)

    def callback(in_data, frame_count, time_info, status):
        global data_int
        data_int = convertDataToArray(in_data)
        #print("{} : {}".format(data_int, len(data_int)))
        return (in_data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    frames_per_buffer=CHUNK,
                    input=True,
                    output=True,
                    input_device_index = idi,
                    output_device_index = odi,
                    stream_callback=callback)

    stream.start_stream()

    print("start")
    
    while (stream.is_active() and not exit_flag):
        try:
            time.sleep(0.05)
        except KeyboardInterrupt:
            print('interrupted')
            break
    
    print("end")
    
    stream.stop_stream()
    stream.close()

    p.terminate()
    
def maintainGraph():
    global data_int
    
    x = np.arange(0, 2*CHUNK, 1)
    y = np.zeros(2*CHUNK)
    
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    line1, = ax.plot(x, y, 'b-')

    plt.axis([0, 2*CHUNK, -40000, 40000])

    while (not exit_flag):
        try:
            line1.set_ydata(data_int)
            # Update graph
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.01)
        except KeyboardInterrupt:
            print('interrupted')
            break

    return
    
if __name__ == "__main__":
    print("started")
    threading.Thread(target=main).start()
    threading.Thread(target=maintainGraph).start()
    while True:
        try:
            time.sleep(0.05)
        except KeyboardInterrupt:
            print('interrupted')
            exit_flag = True
            break
        except:
            print("Error: unable to start thread")
    print("ended")
