from CommonData import *

import matplotlib.pyplot as plt

import sys
import threading
import time

class AudioProcessor:
    
    CHUNK    = 1024
    
    #DEFAULT_ARRAY = np.zeros( 2 * CHUNK )
    DEFAULT_ARRAY = np.zeros( CHUNK )
    
    def __init__(self):
        self._loop_active = True
        self._thread = None
        
        self._data = AudioData()
        
        return
    
    def _processData(self, data):
        data = -data
        return data
    
    def _doProcessLoop(self):
        CHUNK2 = 2 * AudioProcessor.CHUNK
        
        # x = np.arange(0, CHUNK2, 1)
        x = np.arange(0, AudioProcessor.CHUNK, 1)
        data_in = AudioProcessor.DEFAULT_ARRAY
        data_out = AudioProcessor.DEFAULT_ARRAY
        
        plt.ion()
        fig1 = plt.figure()
        fig2 = plt.figure()
        
        ax1 = fig1.add_subplot(1, 1, 1)
        ax2 = fig2.add_subplot(1, 1, 1)
        
        line1, = ax1.plot(x, data_in, 'b--')
        ax1.set_ylim((4000, -4000))
        
        line2, = ax2.plot(x, data_out, 'r--')
        ax2.set_ylim((4000, -4000))

        
        while (self._loop_active):
            data_in = self._data.getDataIn()
            if (data_in is None or len(data_in) != CHUNK2):
                data_in = AudioProcessor.DEFAULT_ARRAY
            data_out = self._processData(data_in)
            if (data_out is None or len(data_out) != CHUNK2):
                data_out = AudioProcessor.DEFAULT_ARRAY
            self._data.setDataOut(data_out)
            
            data_in = data_in[::2]
            data_out = data_out[::2]
            
            line1.set_ydata(data_in)
            line2.set_ydata(data_out)
            
            fig1.canvas.draw()
            fig2.canvas.draw()
            fig1.canvas.flush_events()
            fig2.canvas.flush_events()
            time.sleep(0.01)
        
        plt.close(fig1)
        plt.close(fig2)
        
        return
    
    def startProcessLoop(self):
        if (self._thread is not None):
            if (self._thread.is_alive()):
                return False
            self._thread = None
        
        self._loop_active = True
        self._thread = threading.Thread(target=self._doProcessLoop)
        self._thread.start()
        return True
    
    def haltProcessLoop(self):
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
    audio_processor = AudioProcessor()
    
    audio_processor.startProcessLoop()

    input("blocked; press any key to exit")

    audio_processor.haltProcessLoop()

    return


if __name__ == "__main__":
    _test()
    input("blocked; press any key to continue")
    _test()


