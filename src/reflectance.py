import csv
import h5py
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from colors import Color

def format_reference(path: str) -> np.array:
	file = open(path, "r")
	wavelengths = []
	counts = []
	for line in file:
		entries = line.split()
		entries = [entry.replace(",", ".") for entry in entries]
		wavelengths.append(float(entries[0]))
		counts.append(float(entries[1]))

	return np.array([wavelengths, counts])

def read_data():
	paths = {}
	paths["root"] = "data/reflectance/reflectance-reference/"
	paths["reflectance"] = paths["root"] + "plate-reflectance.xlsx"
	paths["white-reference"] = paths["root"] + "white-reference.txt"
	paths["dark-reference"] = paths["root"] + "background-reference.txt"
	
	reflectance_df = pd.read_excel(paths["reflectance"])
	white_reference_file = open(paths["white-reference"], "r")
	dark_reference_file = open(paths["dark-reference"], "r")

	white_reference = format_reference(paths["white-reference"])
	dark_reference = format_reference(paths["dark-reference"])

	reflectance_df["Wavelength"] = reflectance_df["Wavelength"] \
		.str.replace(',', '.')
	reflectance_df["Ref 1"] = reflectance_df["Ref 1"].str.replace(',', '.')
	reflectance_df["Ref 2"] = reflectance_df["Ref 2"].str.replace(',', '.')
	reflectance_df["Ref 3"] = reflectance_df["Ref 3"].str.replace(',', '.')
	reflectance_df["Ref 4"] = reflectance_df["Ref 4"].str.replace(',', '.')
	reflectance_df["Ref 5"] = reflectance_df["Ref 5"].str.replace(',', '.')

	# 350-1100
	reflectance = (reflectance_df.values.T).astype(np.float)
	mask = np.logical_and(reflectance [0] > 350, reflectance[0] < 1100)
	reflectance = reflectance[:, mask]
	reflectance[1:6] /= 100
	reflectance_means = np.mean(reflectance[1:6], axis=0)
	reflectance_stds = np.std(reflectance[1:6], axis=0)

	reference_fig = plt.figure(figsize=(16, 9))
	plt.subplot(1, 2, 1)
	plt.xlabel("Wavelength [nm]")
	plt.ylabel("Count [-]")
	plt.title("White Reference")
	plt.plot(white_reference[0], white_reference[1])

	plt.subplot(1, 2, 2)
	plt.xlabel("Wavelength [nm]")
	plt.ylabel("Count [-]")
	plt.title("Dark Reference")
	plt.plot(dark_reference[0], dark_reference[1])

	reflectance_fig = plt.figure(figsize=(16, 9))
	plt.subplot(1, 2, 1)
	plt.plot(reflectance[0], reflectance[1], label='Sample 1')
	plt.plot(reflectance[0], reflectance[2], label='Sample 2')
	plt.plot(reflectance[0], reflectance[3], label='Sample 3')
	plt.plot(reflectance[0], reflectance[4], label='Sample 4')
	plt.plot(reflectance[0], reflectance[5], label='Sample 5')
	plt.xlabel("Wavelength [nm]")
	plt.ylabel("Reflectance [-]")
	plt.title("Reference Plate Reflectance Samples")
	plt.legend()

	plt.subplot(1, 2, 2)
	plt.plot(reflectance[0], reflectance_means, 
		color=Color.Blue.value, label="Mean Reflectance")
	plt.plot(reflectance[0], reflectance_means + reflectance_stds,
		color=Color.Red.value, linestyle="dashed", 
		label= "Mean" + r'$\pm$' + "Standard Deviation") 
	plt.plot(reflectance[0], reflectance_means - reflectance_stds, 
		color=Color.Red.value, linestyle="dashed")
	plt.xlabel("Wavelength [nm]")
	plt.ylabel("Reflectance [-]")
	plt.title("Reference Plate Reflectance")
	plt.legend()

	plt.show()

def main():
	read_data()

if __name__ == '__main__':
	main()
