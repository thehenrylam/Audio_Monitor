from CommonData import *

import matplotlib.pyplot as plt

import sys
import threading
import time

class AudioProcessor:
    
    # Parameters of AudioProcessor that shouldn't be touched within the class
    CHUNK    = 1024
    DEFAULT_ARRAY = np.zeros( CHUNK )
    
    def __init__(self):
        # Initialize AudioData() in self._data
        self._data = AudioData()
        
        self._loop_active = True
        self._thread = None
        
        return
    
    # This function returns a numpy array which its values are dependent on its given arguments (np.array())
    def _processData(self, data):
        #data = -data
        return data
    
    # This is the main function that AudioProcessor.py performs
    def _doProcessLoop(self):
        # Initialize CHUNK * 2 to be used to compare values later
        CHUNK2 = 2 * AudioProcessor.CHUNK
        
        # Set default data for plotting
        x = np.arange(0, AudioProcessor.CHUNK, 1)
        data_in = AudioProcessor.DEFAULT_ARRAY
        data_out = AudioProcessor.DEFAULT_ARRAY
        
        # Enable plot interaction
        plt.ion()
        
        # Start two figures (one for input data and one for processed/output data)
        fig1 = plt.figure()
        fig2 = plt.figure()
        
        # Add a sublot to get the axes object for both figures
        ax1 = fig1.add_subplot(1, 1, 1)
        ax2 = fig2.add_subplot(1, 1, 1)
        
        # Plot the input/output data graph with the default values (blue for input and red for output),
        # retrieve the line objects as well
        line1, = ax1.plot(x, data_in, 'b--')
        line2, = ax2.plot(x, data_out, 'r--')
        
        # Set the y axis' range to be max = 4000 and min = -4000
        ax1.set_ylim((4000, -4000))
        ax2.set_ylim((4000, -4000))
        
        # Main loop, breaking the loop gracefully (without ctrl-C) is by setting the _loop_active flag to False by an outside process
        while (self._loop_active):
            # Get the input data from CommonData.py
            data_in = self._data.getDataIn()
            if (data_in is None or len(data_in) != CHUNK2):
                data_in = AudioProcessor.DEFAULT_ARRAY
            
            # Get the output data (processed data) by passing data_in through self._processData
            data_out = self._processData(data_in)
            if (data_out is None or len(data_out) != CHUNK2):
                data_out = AudioProcessor.DEFAULT_ARRAY
            
            # Immediately sent output data to CommonData.py
            self._data.setDataOut(data_out)
            
            # Make the length of both arrays to be of length CHUNK by
            # extracting the value of the array whose index is even.
            data_in = data_in[::2]
            data_out = data_out[::2]
            
            # Set the y data of the graphs to its respective arrays
            line1.set_ydata(data_in)
            line2.set_ydata(data_out)
            
            # Draw each figure's canvases
            fig1.canvas.draw()
            fig2.canvas.draw()
            
            # Flush the events to erase it
            fig1.canvas.flush_events()
            fig2.canvas.flush_events()
            
            # Have the process to sleep to ensure that the program doesn't hog CPU cycles
            time.sleep(0.01)
        
        # Close the plots
        plt.close(fig1)
        plt.close(fig2)
        
        return
    
    # This function performs the same purpose as AudioStream's startStreamLoop(self)
    def startProcessLoop(self):
        if (self._thread is not None):
            if (self._thread.is_alive()):
                return False
            self._thread = None
        
        self._loop_active = True
        self._thread = threading.Thread(target=self._doProcessLoop)
        self._thread.start()
        return True
    
    # This function performs the same purpose as AudioStream's haltStreamLoop(self)
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


