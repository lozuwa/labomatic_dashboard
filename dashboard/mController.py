import os
import sys
import subprocess
import cv2
import numpy as np
# from . import LoadObjectDetectionModel as LoadObjDect
from impy.preprocess import preprocessImage

# Global variables
# obj = LoadObjDect.LoadObjectDetectionModel()
prep = preprocessImage()

def allowed_files(path, files):
	"""
	Filter the files that are allowed. Remove the 
	rest.
	Args:
		path: A string that contains the path to a folder.
		files: A list of strings that contains the names of 
					the files in the current folder.
	Results:
		A list containing the allowed files
	"""
	for file in files:
		if file.endswith(".jpg"):
			continue
		else:
			files.remove(file)
			os.remove(os.path.join(path, file))
	return files

def preprocess_folder(path = None):
	"""
	Given the path of a folder, let's read the files inside and
	preprocess them for classification.
	Args:
		path: A string that contains a path to a folder.
	Returns:
		None
	"""
	# Assertions
	assert type(path) == str
	assert os.path.isdir(path) == True
	# Read files in folder
	files = os.listdir(path)
	# Validate all files
	files = allowed_files(path, files)
	# Preprocess the files
	for file in files:
		preprocess_file(os.path.join(path, file))

def preprocess_file(file):
	"""
	Preprocess an image file for classification.
	Args:
		file: A string that contains the full path to an image file.
	Returns:
		None
	"""
	# Local variables
	path, temp = os.path.split(file)
	file_name = temp.split(".")[0]
	file_ext = temp.split(".")[1]
	width_patches = 4
	height_patches = 3
	# Preprocess iamge
	frame = cv2.imread(file)
	height, width, depth = frame.shape
	patches, nh, nw = prep.divideIntoPatches(image_width=width,
																					image_height=height,
																					padding="VALID_FIT_ALL",
																					number_patches=(width_patches,
																													height_patches))
	# Save file's patches
	for index, patch in enumerate(patches):
		# Create new name
		new_name = "".join([file_name, str(index), ".", file_ext])
		new_name = os.path.join(path, new_name)
		# Decode patch
		iy, ix, y, x = patch
		# Save patch
		cv2.imwrite(new_name, frame[iy:y, ix:x, :])
	# Remove file
	os.remove(file)

def classify_files():
	"""
	Args:
		path: A string that contains the path to a preprocessed folder of images.
	Returns:
		None
	"""
	file_path = os.path.join(os.getcwd(),
													"dashboard/LoadObjectDetectionModel.py")
	p = subprocess.Popen(["python", file_path], stdout=subprocess.PIPE)

# if __name__ == "__main__":
# 	r = classify_files("/home/pfm/Documents/pfm/web/backend/LabomaticModels/media/Ascaris lumbricoides_17_6_12_589278.jpg", 4, 3)
