import cv2
import h5py
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from typing import List, Tuple

from colors import Color
from utilities import print_h5_file, print_group, print_dataset

def get_rgb_frames(path: str) -> Tuple[np.array, np.array]:
	with h5py.File(path, "r") as f:
		rgb = f["rawdata"]["rgb"]
		imgs = np.array(rgb["rgbFrames"])
		ts = np.array(rgb["timestamp"])
		return (ts, imgs)

def watch_rgb_movie(ts, imgs):
	dts = ts[1:] - ts[:-1]
	n = len(imgs)
	print(imgs[0, :, :, 0])
	print(dts.shape)
	plt.figure()
	for i, img in enumerate(imgs):
		cv2.imshow(img)
		cv2.waitKey(33)

def main():
	path = "/home/martin/Data/UHI/uhi_20201117_130806_10.h5"
	prefix = "   "
	displacement = 40

	ts, imgs = get_rgb_frames(path)
	watch_rgb_movie(ts, imgs)

if __name__ == "__main__":
	main()
