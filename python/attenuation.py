import csv
import h5py
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.stats

from typing import List

from utilities import print_h5_file, print_group, print_dataset


plt.style.use(['project-thesis'])

def print_file_structures(root: str, files: List[str]):
	prefix = "   "
	displacement = 40
	for file in files:
		path = root + file
		print("\n{0}:".format(path))
		print_h5_file(path, prefix, displacement)

def read_attenuation_from_hdf5(path: str):
	with h5py.File(path, "r") as f:
		attenuationMeter = f["rawdata"]["waterQuality"]\
			["attenuationMeter"]
		coefficients = np.array(attenuationMeter["attenuation"])
		wavelengths = np.array(attenuationMeter["band2Wavelength"])
		return (wavelengths, coefficients)

def convert_to_csv(paths: List[str]):
	attenuation = []
	wavelengths = None
	for i, path in enumerate(paths):
		if i == 0:
			wavelengths, coefficients = \
				read_attenuation_from_hdf5(path)
		else:
			_, coefficients = \
				read_attenuation_from_hdf5(path)
		attenuation.append(coefficient)

	wavelengths = np.array(wavelengths)
	data = np.concatenate([wavelengths[np.newaxis, :]] + attenuation, 
		axis=0).T
	np.savetxt('./data/beam-attenuation.csv', data, delimiter=',')

def read_attenuation_from_csv(path: str):
	reader = csv.DictReader
	with open(path, newline='') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',')
		data = {}
		for row in reader:
			for key, value in row.items():
				if not key in data:
					data[key] = []
				
				if key == 'wavelength':
					data[key].append(int(value))
				else:
					data[key].append(float(value))

	for key, value in data.items():
		data[key] = np.array(value)

	return data

def plot_attenuation(path: str):
	data = read_attenuation_from_csv(path)
	
	wavelengths = data['wavelength']

	coefficients_location1 = np.stack([
		data['location1_sample1'],
		data['location1_sample2'],
		data['location1_sample3'],
		data['location1_sample4'],
		data['location1_sample5'],
		], axis=0)

	coefficients_location2 = np.stack([
		data['location2_sample1'],
		data['location2_sample2'],
		data['location2_sample3'],
		data['location2_sample4'],
		data['location2_sample5'],
		], axis=0)

	coefficients_location3 = np.stack([
		data['location3_sample1'],
		data['location3_sample2'],
		data['location3_sample3'],
		data['location3_sample4'],
		data['location3_sample5'],
		], axis=0)

	coefficients_location4 = np.stack([
		data['location4_sample1'],
		data['location4_sample2'],
		data['location4_sample3'],
		data['location4_sample4'],
		data['location4_sample5'],
		], axis=0)

	coefficient_means_location1 = np.mean(coefficients_location1, axis=0)
	coefficient_means_location2 = np.mean(coefficients_location2, axis=0)
	coefficient_means_location3 = np.mean(coefficients_location3, axis=0)
	coefficient_means_location4 = np.mean(coefficients_location4, axis=0)

	# Figure 1 - Location means.
	fig1, ax1 = plt.subplots()
	ax1.plot(wavelengths, coefficient_means_location1, 
		label='Location 1')
	ax1.plot(wavelengths, coefficient_means_location2, 
		label='Location 2')
	ax1.plot(wavelengths, coefficient_means_location3, 
		label='Location 3')
	ax1.plot(wavelengths, coefficient_means_location4, 
		label='Location 4')
	ax1.set_xlabel(r'Wavelength, $\lambda$ [nm]')
	ax1.set_ylabel(r'Beam attenuation coefficient, ' \
		+ r'$c$ $[\frac{1}{\text{m}}]$')
	ax1.legend(loc='upper right')
	fig1.savefig('./figures/beam-attenuation-coefficient-samples.png', 
		dpi=300)

	# Concatenate measurements from different locations.
	coefficients = np.concatenate([
		coefficients_location1,
		coefficients_location2,
		coefficients_location3,
		coefficients_location4,
		], axis=0)

	# Statistics.
	n = coefficients.shape[0]
	coefficient_means = np.mean(coefficients, axis=0)
	coefficient_confidences = scipy.stats.t.interval(alpha=0.95, df=n-1, 
		scale=scipy.stats.sem(coefficients, axis=0))

	# Figure 2 - Mean and confidence interval.
	fig2, ax2 = plt.subplots()
	ax2.plot(wavelengths, coefficient_means, label='Mean')
	ax2.plot(wavelengths, coefficient_means + coefficient_confidences[0],
		color='#e6091c', linestyle=':',
		label=r'95\text{\%}-confidence bounds')
	ax2.plot(wavelengths, coefficient_means + coefficient_confidences[1],
		color='#e6091c', linestyle=':')
	ax2.set_xlabel(r'Wavelength, $\lambda$ [nm]')
	ax2.set_ylabel(r'Beam attenuation coefficient, ' \
		+ r'$c$ $[\frac{1}{\text{m}}]$')
	ax2.legend(loc='upper right')
	fig2.savefig('./figures/beam-attenuation-coefficient.png', dpi=300)

	plt.show()

def main():
	path = '/home/martin/project-thesis/data/beam-attenuation/' \
		+ 'beam-attenuation-coefficients.csv'
	plot_attenuation(path)

if __name__ == '__main__':
	main()
