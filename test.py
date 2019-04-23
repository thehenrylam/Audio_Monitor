"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""
from sys import byteorder

import struct
import numpy as np
import matplotlib.pyplot as plt

import time

import pyaudio
import wave

CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

def updateGraph(line, fig, data_int, x):
    line.set_ydata(data_int)
    fig.canvas.draw()
    fig.canvas.flush_events()
    return

def convertDataToArray(data):
    data_int = np.frombuffer(data, dtype=np.int16)
    if byteorder == 'little':
        data_int = data_int.byteswap()
    return data_int

def main():
    fig, ax = plt.subplots()
    x = np.arange(0, CHUNK, 1)
    line, = ax.plot(x, np.random.rand(CHUNK))

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        
        #data_int = convertDataToArray(data)
        #updateGraph(line, fig, data_int, x)
        
        time.sleep(0.01)
        
        #data_int = np.frombuffer(data, dtype=np.int16)
        #if byteorder == 'little':
            #data_int = data_int.byteswap()
        #print(len(data_int))
        #line.set_ydata(data_int)
        #fig.canvas.draw()
        #fig.canvas.flush_events()
        

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # ax.plot(data_int, '-')
    # plt.show()
    return

if __name__ == "__main__":
    main()
