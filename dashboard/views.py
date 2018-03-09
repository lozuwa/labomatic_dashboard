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
REDIRECT_PATH = "dashboard/media/"

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
			# Parse quantitative results
			# Query the results
			listResults = cdb.readResultByID(client_id = client_id)
			# Convert results to a list of hash maps
			summary = []
			for index, result in enumerate(listResults):
				summary.append({"index": index,
												"microorganism": result.property_microorganism,
												"count": result.property_count})
			# Parse images to display
			path_client = os.path.join(os.getcwd(), "dashboard", \
																"media", "dashboard", \
																client_id)
			images = [{"path": os.path.join(path_client, each)} for each in \
														os.listdir(path_client)\
														if os.path.isfile(os.path.join(path_client, each))]
			# Add parameters to context hashmap
			context = {"summary": summary,
									"images": images}
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

# from ClientsDatabaseHandler import *
# cdb = ClientsDatabaseHandler(user = "root", password = "root")
