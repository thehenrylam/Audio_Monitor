from AudioStream import *
from AudioProcessor import *


def main():
    audio_stream = AudioStream()
    audio_processor = AudioProcessor()
    
    audio_stream.setDeviceIndex()
    
    audio_stream.startStreamLoop()
    audio_processor.startProcessLoop()
    
    input("Press any button to exit")
    
    audio_stream.haltStreamLoop()
    audio_processor.haltProcessLoop()
    
    return

if __name__ == "__main__":
    main()
