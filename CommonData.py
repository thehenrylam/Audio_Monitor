# Singleton/
from sys import byteorder

import struct
import numpy as np

# AudioData is a singleton class, it acts like a connector to relay data between AudioProcessor.py and AudioStream.py
class AudioData():
    
    # This is the data that AudioData contains
    _data_in = None
    _data_out = None
    
    def __init__(self):
        return
    
    # This is to enable easy printing of the class's data for debugging
    def __str__(self):
        text = "data_i: {}\ndata_o: {}".format(self._data_in, self._data_out)
        return text
    
    # Convert the data (type = bytes) to a numpy array
    def _convertByteToArray(self, data):
        data_int = np.frombuffer(data, dtype=np.int16)
        
        return data_int
    
    # Set variable AudioData._data_in to the numpy array from the data given in the argument
    def setDataIn(self, data_in):
        if (type(data_in) is bytes):
            AudioData._data_in = self._convertByteToArray(data_in)
        elif (type(data_in) is np.ndarray):
            AudioData._data_in = data_in
            
        return
    
    # Returns the AudioData._data_in
    def getDataIn(self):
        return AudioData._data_in
    
    # Set variable AudioData._data_out to the numpy array from the data given in the argument
    def setDataOut(self, data_out):
        if (type(data_out) is bytes):
            AudioData._data_out = self._convertByteToArray(data_out)
        elif (type(data_out) is np.ndarray):
            AudioData._data_out = data_out
        return
    
    # Returns the AudioData._data_out
    def getDataOut(self):
        return AudioData._data_out

def _test():
    data = AudioData()
    
    in_array = np.array([1, 2, 3])
    ou_array = np.array([7, 8, 9])
    
    data.setDataIn(in_array)
    data.setDataOut(ou_array)
    
    print(data)
    
    print("real_i: {}".format(data.getDataIn()))
    print("real_o: {}".format(data.getDataOut()))
    
    return

    
if __name__ == "__main__":
    _test()
