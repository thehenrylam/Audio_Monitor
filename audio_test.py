
from sys import byteorder

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

def trim(aud_data)
	"Comment"
	def _trim(aud_data):
		number_samples = len(aud_data)/CHUNK
		
		if number_samples <= 0:
			return aud_data
		
		for i in range(number_samples):
			sample = aud_data[CHUNK*i:CHUNK*(i+1)]
			if isSilent(sample):
				aud_data = np.delete(aud_data, [range(CHUNK*i, CHUNK*(i+1))])
			else:
				return
		
		return
	
	aud_data = _trim(aud_data)
	np.flip(aud_data, 0)
	aud_data = _trim(aud_data)
	np.flip(aud_data, 0)
	
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
	
	stream = p.open(format=FORMAT, channels=1, rate=RATE,
				 input=True, output=True,
				 frames_per_buffer=CHUNK)
	
	num_silent = 0
	data = (np.array([])).astype(np.int16)
	
	while 1:
		aud_data = (np.array( stream.read(CHUNK) )).astype(np.int16)
		if byteorder == 'big':
			aud_data.byteswap(inplace = True)
		
		plot_tool.addData(aud_data)
		data = np.append(data, aud_data)
		
		silent = isSilent(aud_data)
		
		#TODO: Need to finish the rest of record()
		break
		
	
	
	return

