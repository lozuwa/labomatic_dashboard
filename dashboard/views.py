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
from .Result import *
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
			# Update this object's status
			cdb.updateClientStatus(Client(client_id=int(client_id), status=1))
			print("Status completed")
			# Run classifier in folder
			classify_files()
			# Render page
			return HttpResponseRedirect("/")
		if client_id != None and int(visualize) == 1:
			# Query the results
			# TODO: organize how to structure the response form 
			# results. There are multiple microorganism and of course multiple
			# counts.
			listResults = cdb.readResultsByID(client_id = client_id)
			result = listResults[0]
			context = {"rows": [i for i in range(2)],
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
		list_clients = cdb.readClients()
		ids = extract_ids(list_clients)
		# Compare clients and folders
		missing_folders = set(folders).difference(set(ids))
		# If there are missing folders, then add 
		# them to the db.
		for folder in missing_folders:
			cdb.createClient(Client(client_id = folder, status = 0))
		# Query clients from db
		list_clients = cdb.readClients()
		# Format clients inside a dictionary
		clients = [{"index": index,
								"id": client.property_client_id,
								"status": "Not diagnosed" if client.property_status == 0 else \
													"Working" if client.property_status == 1 else \
													"Diagnosed"}
							for index, client in enumerate(list_clients)]
		context = {"clients": clients}
		return render(request,
								"dashboard/clients_table.html",
								context)

def refresh(request):
	return HttpResponseRedirect("/")