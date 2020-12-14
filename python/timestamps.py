import h5py
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np

from utilities import print_h5_file, print_group, print_dataset

def main():
	path = "data/attenuation/uhi_20201111_131120_1.h5"
	prefix = "   "
	displacement = 40
	print_h5_file(path, prefix, displacement)

	with h5py.File(path, "r") as f:
		hyperspectral = f["rawdata"]["hyperspectral"]
		timestamps = np.array(hyperspectral["timestamp"])
		exposures = np.array(hyperspectral["exposureTime"])
	
	print(timestamps[0])
	print(timestamps[1])
	print(timestamps[2])
	print(timestamps[3])

	sampling_times = timestamps[1:-1] - timestamps[0:-2]
	fig = plt.figure()
	plt.plot(sampling_times)
	plt.plot(exposures / 1000) # Exposure in seconds.
	plt.show()

	

if __name__ == '__main__':
	main()
