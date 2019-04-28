from AudioStream import *
from AudioProcessor import *

"""
    This is the core script for running the waveform viewer.
    This script ABSOLUTELY requires:
        AudioStream.py
        AudioProcessor.py
        CommonData.py
"""
def main():
    # Initialize AudioStream() and AudioProcessor() objects/classes
    audio_stream = AudioStream()
    audio_processor = AudioProcessor()
    
    # Have the user select the input and output devices for the program to work
    audio_stream.setDeviceIndex()
    
    # Run the AudioStream's and AudioProcessor's respective threads to perform their tasks
    audio_stream.startStreamLoop()
    audio_processor.startProcessLoop()
    
    # This is to block the main thread/process to have a way to exit as gracefully as the program can allow itself
    input("Press any button to exit")
    
    # Halt the two class's respective threads as gracefully as possible
    audio_stream.haltStreamLoop()
    audio_processor.haltProcessLoop()
    
    return

if __name__ == "__main__":
    main()
