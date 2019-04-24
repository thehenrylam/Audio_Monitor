# AudioStream.py
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
        
        return
    
    def setDeviceIndex():
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
        if (i_index != ""):
            try:
                self._input_index = int(i_index)
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
            return (in_data, pyaudio.paContinue)
        
        stream = self._p.open(
                format=self._p.get_format_from_width( AudioStream.WIDTH )
                channels= AudioStream.CHANNELS,
                rate= AudioStream.RATE,
                input= True,
                output= True,
                input_device_index= self._input_index,
                output_device_index= self._output_index,
                stream_callback=callback
            )
        
        stream.start_stream()
        
        self._loop_active = True
        
        while (stream.is_active() and not self._loop_active):
            time.sleep(0.05)
        
        stream.stop_stream()
        stream.close()
        
        self._p.terminate()
        
        return
    
    def startStreamLoop(self):
        threading.Thread(target=self._doStreamLoop).start()
        
        return
    
    def haltStreamLoop(self):
        self._loop_active = False
        
        return
    
    
    
