# Singleton/
from sys import byteorder

import struct
import numpy as np

class AudioData():
    
    _data_in = None
    _data_out = None
    
    def __init__(self):
        return
    
    def __str__(self):
        text = "data_i: {}\ndata_o: {}".format(self._data_in, self._data_out)
        return
    
    def _convertByteToArray(data):
        data_int = np.frombuffer(data, dtype=np.int16)
        
        if byteorder == 'big':
            data_int = data_int.byteswap()
        
        return data_int
    
    def setDataIn(self, data_in):
        if (type(data_in) is byte):
            AudioData._data_in = self._convertByteToArray(data_in)
        elif (type(data_in) is np.ndarray):
            AudioData._data_in = data_in
            
        return
    
    def getDataIn(self):
        return AudioData._data_in
    
    def setDataOut(self, data_out):
        if (type(data_out) is byte):
            AudioData._data_out = self._convertByteToArray(data_out)
        elif (type(data_out) is np.ndarray):
            AudioData._data_out = data_out
        return
    
    def getDataOut(self):
        return AudioData._data_out

def test():
    print("Need to do this!")
    
if __name__ == "__main__":
    test()
