# General purpose
import os
# Django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Local libraries
from .mController import *
# Database
from .ClientsDatabaseHandler import *
from .Client import *
# Utils
from .utils import *

# Constant global variables
cdb = ClientsDatabaseHandler(user="root", password="root")
CLIENTS_PATH = "/home/pfm/Documents/diagnostics/"

def index(request):
	if request.method == "POST":
		# In case we get an id and its viz status
		client_id = request.GET.get("id")
		visualize = request.GET.get("visualize")
		print("Data: ", client_id, visualize)
		if client_id != None and int(visualize) == 0:
			# Convert id to str
			client_id = str(client_id)
			# Preprocess the folder
			path_to_id = os.path.join(CLIENTS_PATH, client_id)
			preprocess_folder(path_to_id)
			# Run classifier in folder
			# results = classify_files(path_to_id)
			# Update this object's status
			cdb.updateClientStatus(Client(client_id=int(client_id), status=1))
			# Render page
			return HttpResponse("asdffads")
		if client_id != None and int(visualize) == 1:
			# Query the results
			# TODO: Replace hardcoded values by db queries
			context = {"rows": [i for i in range(2)],
								"cols": [i for i in range(4)],
								"summary": [{"index": i,
														"parasite":"Ascaris",
														"quantity":"3"} for i in range(1)]}
			return render(request,
									"dashboard/show_client.html",
									context)
	else:
		# Get folders from path
		folders = os.listdir(CLIENTS_PATH)
		# Query clients from db
		clients = cdb.readClients()
		ids = extract_ids(clients)
		# Compare clients and folders
		missing_folders = set(folders).difference(set(ids))
		# If there are missing folders, then add 
		# them to the db.
		for folder in missing_folders:
			cdb.createClient(Client(client_id = folder, status = 0))
		# Query clients from db
		clients = cdb.readClients()
		clients_formatted = format_ids_status(clients)
		# Format clients inside a dictionary
		clients = [{"index": index,
								"id": key,
								"status": clients_formatted.get(key)}
							for index, key in enumerate(clients_formatted)]
		for client in clients:
			st = client["status"]
			if st == 0:
				client["status"] = "Diagnosed"
			elif st == 1:
				client["status"] = "Working"
			elif st == 2:
				client["status"] = "Diagnosed"
			else:
				pass
		context = {"clients": clients}
		return render(request,
								"dashboard/clients_table.html",
								context)

def refresh(request):
	return HttpResponseRedirect("/")