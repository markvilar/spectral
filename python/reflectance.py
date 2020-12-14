import csv
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.signal
import scipy.stats

plt.style.use(['project-thesis'])

def read_csv(path: str):
	reader = csv.DictReader
	with open(path, newline='') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',')
		data = {}
		for row in reader:
			for key, value in row.items():
				if not key in data:
					data[key] = []
				
				if key == 'background' or key == 'reference':
					data[key].append(int(value))
				else:
					data[key].append(float(value))

	for key, value in data.items():
		data[key] = np.array(value)

	return data

def plot_reflectance(path: str):
	data = read_csv(path)

	# Extract relevant data.
	wavelengths = data['wavelength']
	reflectances = np.stack([
		data['reflectance_1'],
		data['reflectance_2'],
		data['reflectance_3'],
		data['reflectance_4'],
		data['reflectance_5'],
		])

	# Logical filtering.
	range_mask = np.logical_and(wavelengths > 350, wavelengths < 1100)
	value_mask = np.logical_not(np.any(reflectances < 0, axis=0))
	mask = np.logical_or(range_mask, value_mask)

	wavelengths = wavelengths[mask]
	reflectances = reflectances[:, mask]
	backgrounds = data['background'][mask]
	references = data['reference'][mask]

	# Median filtering.
	filter_size = 9
	backgrounds = scipy.signal.medfilt(backgrounds, filter_size)
	references = scipy.signal.medfilt(references, filter_size)

	# Reflectance statistics - Mean and CI
	n = reflectances.shape[0]
	reflectance_means = np.mean(reflectances, axis=0)
	reflectance_confidences = scipy.stats.t.interval(alpha=0.95, df=n-1, 
		scale=scipy.stats.sem(reflectances, axis=0))

	print(reflectance_means.shape)
	print(reflectance_confidences[0].shape)
	print(reflectance_confidences[1].shape)

	# Figure 1 - White Reference
	fig1, ax1 = plt.subplots(figsize=(3, 3))
	ax1.plot(wavelengths, backgrounds)
	ax1.set_xlabel("Wavelength $\lambda$ [nm]")
	ax1.set_ylabel(r"Intensity count, $I_{\text{background}}$ [-]")
	fig1.savefig('./figures/background-intensity.png', dpi=300)

	# Figure 2 - Dark Reference
	fig2, ax2 = plt.subplots(figsize=(3, 3))
	ax2.plot(wavelengths, references)
	ax2.set_xlabel(r'Wavelength, $\lambda$ [nm]')
	ax2.set_ylabel(r'Intensity count, $I_{\text{ref}}$ [-]')
	fig2.savefig('./figures/reference-intensity.png', dpi=300)

	# Figure 3 - Reflectance Samples
	fig3, ax3 = plt.subplots()
	ax3.plot(wavelengths, reflectances[0], label='Sample 1')
	ax3.plot(wavelengths, reflectances[1], label='Sample 2')
	ax3.plot(wavelengths, reflectances[2], label='Sample 3')
	ax3.plot(wavelengths, reflectances[3], label='Sample 4')
	ax3.plot(wavelengths, reflectances[4], label='Sample 5')
	ax3.set_xlabel(r'Wavelength, $\lambda$ [nm]')
	ax3.set_ylabel(r'Relative reflectance, $\frac{L_{u}}{L_{u, ref}}$ [-]')
	ax3.legend(loc='lower right')
	fig3.savefig('./figures/relative-reflectance-samples.png', dpi=300)

	# Figure 4 - Reflectance Mean
	fig4, ax4 = plt.subplots()
	ax4.plot(wavelengths, reflectance_means, label='Mean')
	ax4.plot(wavelengths, reflectance_means + reflectance_confidences[0],
		color='#e6091c', linestyle=':',
		label=r'95\text{\%}-confidence bounds') 
	ax4.plot(wavelengths, reflectance_means + reflectance_confidences[1], 
		color='#e6091c', linestyle=':')
	ax4.set_xlabel(r'Wavelength, $\lambda$ [nm]')
	ax4.set_ylabel(r'Relative reflectance, $\frac{L_{u}}{L_{u, ref}}$ [-]')
	ax4.legend(loc='lower right')
	fig4.savefig('./figures/relative-reflectance.png', dpi=300)
	plt.show()

def main():
	plot_reflectance('/home/martin/project-thesis/data/'
		+ 'relative-reflectance/relative-reflectance.csv')

if __name__ == '__main__':
	main()
