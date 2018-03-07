import os
import sys

def extract_ids(clients):
	return [i[1] for i in clients]

def format_ids_status(clients):
	d = {}
	for client in clients:
		d[client[1]] = client[2]
	return d
