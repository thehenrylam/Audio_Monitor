# AudioStream.py
from CommonData import *

import struct
import pyaudio
import wave
import threading
import time

"""
    AudioStream.py is a file that contains an individual class and test function,
    This file is supposed to be focused on gathering input data and exporting output data.
    
    For this file to work properly, the file needs:
        CommonData.py
"""
class AudioStream:
    
    # This is the global variables that AudioStream() should ALWAYS have and shouldn't be changed within the class
    CHUNK    = 1024
    WIDTH    = 2
    CHANNELS = 2
    RATE     = 44100
    
    def __init__(self):
        # Initialize the class PyAudio()
        self._p = pyaudio.PyAudio()
        
        # Initiallize the class AudioData()
        self._data = AudioData()
        
        # Have the input and output index be None so that it can choose its default if setDevieIndex() isn't called beforehand
        self._input_index = None
        self._output_index = None
        
        # Set the loop flag to True to gaurantee that doStreamLoop() doesn't pass through the main while loop
        self._loop_active = True
        
        # Set the thread variable to None so that haltStreamLoop() will do nothing if called before startStreamLoop()
        self._thread = None
        
        return
    
    # Function that prints the all the devices and their indices, then prompts the user to select the devices used for input and output
    def setDeviceIndex(self):
        device_count = self._p.get_device_count()
        
        # Print out device's IO information to the user
        for i in range(device_count):
            device_info = self._p.get_device_info_by_index(i)
            print("{}\t : {}/{}".format(
                device_info['index'],
                device_info['name'],
                device_info['defaultSampleRate']
                ))
        # Set the input/output indices to be its default
        self._input_index = self._p.get_default_input_device_info()['index']
        self._output_index = self._p.get_default_output_device_info()['index']
        
        # Have the user select the program's input
        i_input = input("What input device should be used? (default: {})\n".format(self._input_index))
        if (i_input != ""):
            try:
                # if the input is outside the range of the device indices, then don't update self._input_index
                if (int(i_input) >= 0 and int(i_input) < device_count):
                    self._input_index = int(i_input)
            except:
                pass
        
        # Have the user select the program's output
        i_output = input("What output device should be used? (default: {})\n".format(self._output_index))
        if (i_output != ""):
            try:
                # if the output is outside the range of the device indices, then don't update self._output_index
                if (int(i_output) >= 0 and int(i_output) < device_count):
                    self._output_index = int(i_output)
            except:
                pass
        
        return
    
    # This function houses the main loop for retrieving and sending data to for the input and output channels
    # The method a which it does so is via callback
    def _doStreamLoop(self):
        
        # Callback function for the stream to call to if the devices are ready
        def callback(in_data, frame_count, time_info, status):
            # Send the data from the input device straight to CommonData() class
            self._data.setDataIn(in_data)
            
            # Retrieve the specified output data from CommonData()
            tmp_data = self._data.getDataOut()
            
            # If the data retrieve isn't None, convert the numpy array back into byte form to be sent out
            if (tmp_data is not None):
                in_data = tmp_data.tobytes()
            
            return (in_data, pyaudio.paContinue)
        
        # Open up the audio stream with the parameters given
        stream = self._p.open(
                format=self._p.get_format_from_width( AudioStream.WIDTH ),
                channels= AudioStream.CHANNELS,
                rate= AudioStream.RATE,
                input= True,
                output= True,
                input_device_index= self._input_index,
                output_device_index= self._output_index,
                stream_callback=callback
            )
        
        # Start up the stream
        stream.start_stream()
        
        # Stop the thread/process from progressing anymore so that callback could occur
        # The main way the loop breaks is if self._loop_active is set to false by an outside process
        while (stream.is_active() and self._loop_active):
            # have the thread/process sleep to ensure that it doesn't hog CPU cycles like a spin lock
            time.sleep(0.1)
        
        # Termination sequence of the stream object
        stream.stop_stream()
        stream.close()
        
        # Terminate PyAudio()
        self._p.terminate()
        
        return
    
    # This function's main purpose is to create a thread that primarily performs the function of self._doStreamLoop()
    def startStreamLoop(self):
        # This block of code ensures that only ONE thread exits to perform the stream loop
        if (self._thread is not None):
            # If self._thread isn't None, give it a second chance and check if the thread is still alive,
            # If it is, then return False (Failure to start loop), if not, then continue through and set self._thread = None
            if (self._thread.is_alive()):
                return False
            self._thread = None
        
        # Perform the thread execution sequence
        self._loop_active = True
        self._thread = threading.Thread(target=self._doStreamLoop)
        self._thread.start()
        
        return True
    
    # This function's main purpose is to terminate a thread (if there is one) the primarily performs the function of self._doStreamLoop()
    def haltStreamLoop(self):
        # This block of code ensures that self._thread is not None and is still alive for it to properly terminate
        if (self._thread is None):
            return False
        elif (not self._thread.is_alive()):
            self._thread = None
            return False
        
        # Perform the thread termination sequence
        self._loop_active = False
        self._thread.join(timeout = 1)
        self._thread = None

        return

def _test():
    audio_stream = AudioStream()
    
    audio_stream.setDeviceIndex()
    
    audio_stream.startStreamLoop()
    
    input("blocked; press any key to exit")
    
    audio_stream.haltStreamLoop()
    
if __name__ == "__main__":
    _test()
    
    
