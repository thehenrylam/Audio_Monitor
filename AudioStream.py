# AudioStream.py
from CommonData import *

import struct
import pyaudio
import wave
import threading
import time

class AudioStream:
    
    CHUNK    = 1024
    WIDTH    = 2
    CHANNELS = 2
    RATE     = 44100
    
    def __init__(self):
        self._p = pyaudio.PyAudio()
        
        self._input_index = None
        self._output_index = None
        
        self._loop_active = True
        self._thread = None
        
        self._data = AudioData()
        
        return
    
    def setDeviceIndex(self):
        #print(self._p.get_device_info_by_index(0))
        
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
                self._input_index = int(i_input)
            except:
                pass
        
        # Have the user select the program's output
        i_output = input("What output device should be used? (default: {})\n".format(self._output_index))
        if (i_output != ""):
            try:
                self._output_index = int(i_output)
            except:
                pass
        
        return
    
    def _doStreamLoop(self):
        
        def callback(in_data, frame_count, time_info, status):
            self._data.setDataIn(in_data)
            tmp_data = self._data.getDataOut()
            if (tmp_data is not None):
                in_data = tmp_data.tobytes()
            
            return (in_data, pyaudio.paContinue)
        
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
        
        stream.start_stream()
                
        while (stream.is_active() and self._loop_active):
            time.sleep(0.1)
        
        stream.stop_stream()
        stream.close()
        
        self._p.terminate()
        
        return
    
    def startStreamLoop(self):
        if (self._thread is not None):
            if (self._thread.is_alive()):
                return False
            self._thread = None
        
        self._loop_active = True
        self._thread = threading.Thread(target=self._doStreamLoop)
        self._thread.start()
        return True
    
    def haltStreamLoop(self):
        if (self._thread is None):
            return False
        elif (not self._thread.is_alive()):
            self._thread = None
            return False            
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
    
    
