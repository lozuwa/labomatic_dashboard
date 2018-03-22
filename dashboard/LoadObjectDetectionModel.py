# AI stuff
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from PIL import Image
import cv2
from collections import Counter

# Database stuff
from ClientsDatabaseHandler import *
from Client import *
from Result import *
from Microorganism import *
from utils import *

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("/home/pfm/Documents/models/research/object_detection/utils/")
import label_map_util
import visualization_utils as vis_util
# from utils import label_map_util
# from utils import visualization_utils as vis_util

class LoadObjectDetectionModel(object):
	# Constructor
	def __init__(self):
		super(LoadObjectDetectionModel, self).__init__()
		# Path to graph and labels
		self.PATH_TO_CKPT = "dashboard/static/assets/frozen_inference_graph.pb"
		self.PATH_TO_LABELS = "dashboard/static/assets/label_map.pbtxt"
		# Number of classes
		self.NUM_CLASSES = 3
		# Load graph and labels
		self.loadGraph()
		self.loadLabels()

	def loadGraph(self):
		self.detection_graph = tf.Graph()
		with self.detection_graph.as_default():
			od_graph_def = tf.GraphDef()
			with tf.gfile.GFile(self.PATH_TO_CKPT, "rb") as fid:
				serialized_graph = fid.read()
				od_graph_def.ParseFromString(serialized_graph)
				tf.import_graph_def(od_graph_def, name="")

	def loadLabels(self):
		label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
		categories = label_map_util.convert_label_map_to_categories(label_map,
																					max_num_classes=self.NUM_CLASSES,
																					use_display_name=True)
		self.category_index = label_map_util.create_category_index(categories)

	def loadImageIntoNumpyArray(self, image):
		(im_width, im_height) = image.size
		return np.array(image.getdata()).reshape(
				(im_height, im_width, 3)).astype(np.uint8)

	def classifyFiles(self, imagePaths = None, thresholdScore = None):
		# Assertions
		if imagePaths == None:
			raise Exception("Image paths cannot be empty")
		if thresholdScore == None:
			thresholdScore = 0.1
		# Local variables
		results = {}
		# Actual detection
		with self.detection_graph.as_default():
			with tf.Session(graph=self.detection_graph) as sess:
				# Definite input and output Tensors for detection_graph
				image_tensor = self.detection_graph.get_tensor_by_name("image_tensor:0")
				# Each box represents a part of the image where a particular object was detected.
				detection_boxes = self.detection_graph.get_tensor_by_name("detection_boxes:0")
				# Each score represent how level of confidence for each of the objects.
				# Score is shown on the result image, together with the class label.
				detection_scores = self.detection_graph.get_tensor_by_name("detection_scores:0")
				detection_classes = self.detection_graph.get_tensor_by_name("detection_classes:0")
				num_detections = self.detection_graph.get_tensor_by_name("num_detections:0")
				for image_path in imagePaths[:]:
					print(image_path)
					image = Image.open(image_path)
					# the array based representation of the image will be used later in order to prepare the
					# result image with boxes and labels on it.
					image_np = self.loadImageIntoNumpyArray(image)
					# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
					image_np_expanded = np.expand_dims(image_np, axis=0)
					# Actual detection.
					(boxes, scores, classes, num) = sess.run(
							[detection_boxes, detection_scores, detection_classes, num_detections],
							feed_dict={image_tensor: image_np_expanded})
					if max(np.squeeze(scores)) > thresholdScore:
						# Visualization of a detection's results.
						vis_util.visualize_boxes_and_labels_on_image_array(image_np,
																		np.squeeze(boxes),
																		np.squeeze(classes).astype(np.int32),
																		np.squeeze(scores),
																		self.category_index,
																		min_score_thresh=thresholdScore,
																		use_normalized_coordinates=True,
																		line_thickness=4)
						# Save file
						im = Image.fromarray(np.uint8(image_np))
						# Extract name and folder
						dir_, filename = os.path.split(image_path)
						dir_, folder = os.path.split(dir_)
						# Save image at new path
						new_image_path = os.path.join(os.getcwd(), "dashboard",\
																				"static", "diagnosis",\
																				folder, filename)
						im.save(new_image_path)
						# Append the results
						# Squeeze vectors to one dimension
						scores = np.squeeze(scores)
						classes = np.squeeze(classes)
						# Find the indexes of scores above threshold
						indexes = np.where(scores > thresholdScore)[0]
						# Count each class' frequency
						frequency = Counter(classes[indexes])
						# Append
						keys = [i for i in frequency.keys()]
						values = [i for i in frequency.values()]
						for key in keys:
							getKey = results.get(key, None)
							if getKey == None:
								results[key] = frequency.get(key, 0)
							else:
								print(frequency.get(key, 0))
								results[key] += frequency.get(key, 0)
					# Remove all files
					os.remove(image_path)
		# Return results
		return results

if __name__ == "__main__":
	# Create a database instance
	cdb = ClientsDatabaseHandler(user = "root", password = "root")
	# Query all clients that require a status 1
	list_clients = cdb.readClientByStatus(status = 1)
	result = list_clients[0]
	client_id = str(result.property_client_id)
	client_status = result.property_status
	# Create folder at media
	create_folder(os.path.join(os.getcwd(), "dashboard", \
														"static", "diagnosis", \
														client_id))
	# Create an object detection instance
	obj = LoadObjectDetectionModel()
	# Read files in the target folder
	path_to_client = os.path.join(CLIENTS_PATH, client_id)
	files = os.listdir(path_to_client)
	# Create a list with the full paths to the images
	image_paths = []
	for file in files:
		image_paths.append(os.path.join(path_to_client, file))
	detectionResults = obj.classifyFiles(imagePaths = image_paths)
	print(detectionResults)
	# Create a result instance attached to the client
	for key in detectionResults:
		mic = cdb.readMicroorganismByID(id_ = key)
		count = detectionResults.get(key, 0)
		cdb.createResult(result = Result(client_id = client_id,
																			microorganism = mic.property_name,
																			count = count))
	# Update the client's status
	cdb.updateClientStatus(client = Client(client_id = client_id,
																					status = 2))

