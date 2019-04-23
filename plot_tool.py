from array import array

import matplotlib.pyplot as plt
import numpy as np
import random

class PlotTool:
	'Plot tool used to help easily convert the data format from pyaudio into a plotable format'
	
	def __init__(self, chunksize):
		self.cs = chunksize
		self.t = 0
		self.y = [(np.array([])).astype(np.int16) for i in range(chunksize)]
	
	def addData(self, data):
		if len(data) != self.cs:
			raise IndexError("The length of the data and set chunksize doesn't match \n"
				"data = {}\n"
				"self.cs = {}".format(data, self.cs))
		for i in range(len(self.y)):
			self.y[i] = np.append(self.y[i], data[i])
		self.t += 1
	
	def show(self):
		t_list = np.array([i for i in range(0, self.t)])
		for i in range(len(self.y)):
			plt.plot(t_list, self.y[i])
		plt.xlabel('time')
		plt.ylabel('sound intensity')
		
		plt.show()


if __name__ == '__main__':
	plot_tool = PlotTool(16)
	
	tmp = [0 for i in range(16)]
	plot_tool.addData(tmp)
	
	for i in range(20):
		tmp = [random.randint(-100, 100) for i in range(16)]
		plot_tool.addData(tmp)
	
	tmp = [0 for i in range(16)]
	plot_tool.addData(tmp)
	
	plot_tool.show()
	
