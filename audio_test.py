
from sys import byteorder
from array import array
from struct import pack

import plot_tool as pt
import numpy as np

import os
import sys
import pyaudio
import wave

THRESHOLD  = 500
CHUNK      = 1024
FORMAT     = pyaudio.paInt16
RATE       = 44100

plot_tool = pt.PlotTool(CHUNK)

def isSilent(aud_data):
	"Returns 'True' if the highest value of audio sample is below THRESHOLD"
	return max(aud_data) < THRESHOLD

def normalize(aud_data):
	"Comment"
	MAXIMUM = 16384
	times = float(MAXIMUM)/max(abs(max(aud_data)), abs(min(aud_data)))
	
	return times * aud_data

def trim(aud_data):
	"Comment"
	def _trim(aud_data):
		number_samples = int(len(aud_data)/CHUNK)
		
		if number_samples <= 0:
			return aud_data
		
		for i in range(number_samples):
			sample = aud_data[CHUNK*i:CHUNK*(i+1)]
			if isSilent(sample):
				aud_data = np.delete(aud_data, [range(CHUNK*i, CHUNK*(i+1))])
			else:
				return
		
		return
	print(aud_data)
	aud_data = _trim(aud_data)
	aud_data = np.flip(aud_data, 0)
	aud_data = _trim(aud_data)
	aud_data = np.flip(aud_data, 0)
	
	return aud_data

def addSilence(aud_data, sec):
	sil = (np.zeros(seconds*RATE)).astype(np.int16)
	aud_data = np.append(sil, aud_data)
	aud_data = np.append(aud_data, sil)
	
	return aud_data

def record():
	"""
	Comment
	"""
	pa = pyaudio.PyAudio()
	
	stream = pa.open(format=FORMAT, channels=1, rate=RATE,
				 input=True, output=True,
				 frames_per_buffer=CHUNK)
	
	num_silent = 0
	aud_started = False
	
	data = (np.array([])).astype(np.int16)
	print("\n\n\nStarted\n\n\n")
	while 1:
		tmp = array('h', stream.read(CHUNK))
		#aud_data = (np.array( tmp )).astype(np.int16)
		if byteorder == 'big':
			tmp.byteswap()
			#aud_data.byteswap(inplace = True)
		
		aud_data = np.array(tmp)
		
		print(aud_data)
		
		plot_tool.addData(aud_data)
		
		continue
		
		data = np.append(data, aud_data)
		
		silent = isSilent(aud_data)
		
		if silent and aud_started:
			num_silent += 1
		elif not silent and not aud_started:
			aud_started = True
		
		if aud_started and num_silent > 20:
			break
	return
	print("\n\n\nEnd\n\n\n")
	sample_width = pa.get_sample_size(FORMAT)
	stream.stop_stream()
	stream.close()
	pa.terminate()
	
	data = normalize(data)
	data = trim(data)
	r = addSilence(r, 1)
	
	return sample_width, data
	
def record_to_file(path):
	sample_width, data = record()
	
	data = pack('<' + ('h'*len(data), *data))
	
	wf = wave.open(path, 'wb')
	wf.setnchannels(1)
	wf.setsamplewidth(sample_width)
	wf.setframerate(RATE)
	wf.writeframes(data)
	
	wf.close()
	return

if __name__ == '__main__':
	print("Started")
	# record_to_file('test.wav')
	record()
	print("Finished")
	plot_tool.show()
