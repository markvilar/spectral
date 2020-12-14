import h5py
import numpy as np
import os

def print_h5_file(path: str, prefix: str, displacement: int):
	with h5py.File(path, "r") as f:
		print(f.filename)
		for key, value in f.items():
			if isinstance(value, h5py.Dataset):
				print_dataset(
					value, 
					prefix + " " + key,
					displacement
					)
			elif isinstance(value, h5py.Group):
				print(prefix + " {}".format(key))
				print_group(
					value, 
					prefix + prefix, 
					prefix,
					displacement
					)
		
def print_group(group: h5py.Group, prefix: str, char: str, displacement: int):
	for key, value in group.items():
		if isinstance(value, h5py.Dataset):
			print_dataset(
				value, 
				prefix + " " + key,
				displacement
				)
		elif isinstance(value, h5py.Group):
			print(prefix + " {}".format(key))
			print_group(
				value, 
				prefix + char, 
				char,
				displacement
				)
	
def print_dataset(dataset: h5py.Dataset, prefix: str, displacement: int):
	diff = displacement - len(prefix)
	if diff > 0:
		print(
			prefix + (" " * diff) + " shape: {}, dtype: {}".format(
			dataset.shape, dataset.dtype)
			)
	else:
		print(
			prefix + "\tshape: {}, dtype: {}".format(
			dataset.shape, dataset.dtype)
			)

def main():
	file_path = "/home/martin/Data/UHI/uhi_20201117_130806_1.h5"
	prefix = "   "
	displacement = 40
	print_h5_file(file_path, prefix, displacement)
	
if __name__ == "__main__":
	main()
