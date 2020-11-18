import h5py
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from typing import List

from colors import Color
from utilities import print_h5_file, print_group, print_dataset

def print_file_structures(root: str, files: List[str]):
	prefix = "   "
	displacement = 40
	for file in files:
		path = root + file
		print("\n{0}:".format(path))
		print_h5_file(path, prefix, displacement)

def get_attenuation(path: str):
	with h5py.File(path, "r") as f:
		attenuationMeter = f["rawdata"]["waterQuality"]\
			["attenuationMeter"]
		attenuation = np.array(attenuationMeter["attenuation"])
		wavelengths = np.array(attenuationMeter["band2Wavelength"])
		return (attenuation, wavelengths)

def plot_attenuation(root: str, files: List[str]):
	paths = [root + file for file in files]
	attenuations = []
	wavelengths = None
	for i, path in enumerate(paths):
		if i == 0:
			attenuation, wavelengths = get_attenuation(path)
		else:
			attenuation, _ = get_attenuation(path)
		attenuations.append(attenuation)

	wavelengths = np.array(wavelengths)
	n_datasets = len(files)

	# Plot raw data
	fig = plt.figure(figsize=(16, 9))
	for i, attenuation in enumerate(attenuations):
		plt.subplot(2, n_datasets//2, i+1)
		plt.plot(wavelengths, attenuation.T)
		plt.ylim([-0.05, 0.2])
		plt.xlabel("Wavelength [nm]")
		plt.ylabel("Attenuation Coefficient [1/m]")
		plt.title("Attenuation Measurements, Location {0}".format(i+1))

	# Plot means and standard deviations
	fig = plt.figure(figsize=(16, 9))
	for i, attenuation in enumerate(attenuations):
		attenuation_means = np.mean(attenuation, axis=0)
		attenuation_stds = np.std(attenuation, axis=0)

		plt.subplot(2, n_datasets//2, i+1)
		plt.plot(wavelengths, attenuation_means, color=Color.Blue.value,
			label="Mean")
		plt.plot(wavelengths, attenuation_means + attenuation_stds,
			color=Color.Red.value, linestyle="dashed")
		plt.plot(wavelengths, attenuation_means - attenuation_stds,
			color=Color.Red.value, linestyle="dashed", 
			label="Mean" + r'$\pm$' + "Standard Deviation")
		plt.ylim([-0.05, 0.2])
		plt.xlabel("Wavelength [nm]")
		plt.ylabel("Attenuation Coefficient [1/m]")
		plt.title("Attenuation, Location {0}".format(i+1))
		plt.legend()

	plt.show()

def main():
	root = "data/attenuation/"
	paths = [
		# 1 - 6 samples
		"uhi_20201111_131257_1.h5",
		# 2 - 6 samples
		"uhi_20201111_132005_1.h5",
		# 3 - 5 samples
		"uhi_20201111_132005_2.h5",
		# 4 - 6 samples
		"uhi_20201111_132709_1.h5",
		]
	#print_file_structures(root, paths)
	plot_attenuation(root, paths)

if __name__ == "__main__":
	main()
