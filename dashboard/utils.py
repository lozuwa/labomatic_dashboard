import os
import sys
from .Client import *

def extract_ids(list_clients):
	ids = []
	for client in list_clients:
		ids.append(client.property_client_id)
	return ids
