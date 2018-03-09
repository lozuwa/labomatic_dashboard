"""
Author: Rodrigo Loza
Company: Labomatic
Description: Util functions for the backend.
"""
import os
import sys
try:
	from .Client import *
except:
	from Client import *

# Constant variables
CLIENTS_PATH = "/home/pfm/Documents/diagnostics/"

def create_folder(path_to_folder):
	"""
	Create a folder.
	Args:
		path_to_folder: A string that contains the path to a folder.
	Returns:
		A boolean. If True, then the folder was created.
		If false, then the folder was not created.
	"""
	# Create folder
	if os.path.isdir(path_to_folder):
		print("Folder already exists.")
	else:
		try:
			os.mkdir(path_to_folder)
		except:
			return False
	return True


def extract_ids(list_clients):
	"""
	Extract the id field from a list of Objects of type
	Client.
	Args:
		list_clients: A list containing objects of type
						client.
	Returns:
		A list of ints that contains the ids of the objects.
	"""
	ids = []
	for client in list_clients:
		ids.append(client.property_client_id)
	return ids

