# Mysql
import pymysql
# Local classes
# TODO: too verbose, it might be better to start the Popen
# process as a python -m package.module to avoid this ugly code.
try:
	from .Client import *
except:
	from Client import *
try:
	from .Result import *
except:
	from Result import *
try:
	from .Microorganism import *
except:
	from Microorganism import *

class ClientsDatabaseHandler(object):
	"""docstring for ClientsDatabaseHandler"""
	# Constructor
	def __init__(self, 
							connection = None, 
							user = None,
							password = None):
		super(ClientsDatabaseHandler, self).__init__()
		# Assertions
		if connection == None:
			connection = "localhost"
		if user == None:
			raise Exception("User cannot be empty")
		if password == None:
			raise Exception("User cannot be empty")
		# Database
		self.databaseName = "labomaticClients"
		self.connection = connection
		self.user = user
		self.password = password
		# Tables
		# clients
		self.CLIENTS_TABLE = "clients"
		self.KEY_ID_CLIENTS = "client_id"
		self.KEY_STATUS_CLIENTS = "status"
		# results
		self.RESULTS_TABLE = "results"
		self.KEY_ID_RESULTS = "client_id"
		self.KEY_MICROORGANISM_RESULTS = "microorganism"
		self.KEY_COUNT_RESULTS = "count"
		# Static table
		# microorganisms
		self.MICROORGANISMS_TABLE = "microorganisms"
		self.KEY_ID_MICROORGANISMS = "id"
		self.KEY_NAME_MICROORGANISMS = "name"

	# CRUD operations for clients table
	def createClient(self, client = None):
		# Assertions
		if client == None:
			raise Exception("client object cannot be empty")
		# Make a connection to the db
		db = pymysql.connect(self.connection,
												self.user,
												self.password,
												self.databaseName)
		cursor = db.cursor()
		# Prepare sql query
		sql = "INSERT INTO {}({}, {})".format(self.CLIENTS_TABLE,
																					self.KEY_ID_CLIENTS,
																					self.KEY_STATUS_CLIENTS)\
					+	" VALUES({}, {});".format(client.property_client_id,
																				client.property_status)
		#print("SQL: ", sql)
		# Execute sql
		try:
			# Execute sql
			cursor.execute(sql)
			# Commit changes to database
			db.commit()
		except:
			# Rollback in case there is any error
			db.rollback()
		# Close db
		db.close()

	def readClients(self):
		# Local variables
		listClients = []
		# Make a connection to the db
		db = pymysql.connect(self.connection,
												self.user,
												self.password,
												self.databaseName)
		cursor = db.cursor()
		# Prepare sql
		sql = "SELECT * FROM {};".format(self.CLIENTS_TABLE)
		#print("SQL: ", sql)
		try:
			# Execute sql
			cursor.execute(sql)
			# Fetch all rows in a list of lists
			results = cursor.fetchall()
			# Append to list of Clients
			for result in results:
				listClients.append(Client(client_id = result[1],
																	status = result[2]))
		except:
			print("Unable to fetch data")
		# Close db connection
		db.close()
		# Return
		return listClients

	def readClientByID(self, client_id = None):
		# Loca variables
		listClients = []
		# Assertions
		if client_id == None:
			raise Exception("Client ID cannot be empty")
		# Make a connection to the db
		db = pymysql.connect(self.connection,
												self.user,
												self.password,
												self.databaseName)
		cursor = db.cursor()
		# Prepare sql
		sql = "SELECT * FROM {}".format(self.CLIENTS_TABLE)\
						+ " WHERE {}={};".format(self.KEY_ID_CLIENTS, client_id)
		#print("SQL: ", sql)
		try:
			# Execute sql
			cursor.execute(sql)
			# Fetch all rows in a list of lists
			results = cursor.fetchall()
			# Append results to a list of Clients
			for result in results:
				listClients.append(Client(client_id = result[1],
																	status = result[2]))
		except:
			print("Unable to fetch data")
		# Close db connection
		db.close()
		# Return
		return listClients

	def readClientByStatus(self, status = None):
		# Local variables
		listClients = []
		# Assertions
		if status == None:
			raise Exception("Status cannot be empty")
		# Make a connection to the db
		db = pymysql.connect(self.connection,
												self.user,
												self.password,
												self.databaseName)
		cursor = db.cursor()
		# Prepare sql
		sql = "SELECT * FROM {}".format(self.CLIENTS_TABLE)\
						+ " WHERE {}={};".format(self.KEY_STATUS_CLIENTS,
																		status)
		#print("SQL: ", sql)
		try:
			# Execute sql
			cursor.execute(sql)
			# Fetch all rows in a list of lists
			results = cursor.fetchall()
			# Append results to list of Clients
			for result in results:
				listClients.append(Client(client_id = result[1],
																	status = result[2]))
		except:
			print("Unable to fetch data")
		# Close db connection
		db.close()
		# Return
		return listClients

	def updateClientStatus(self, client = None):
		# Assertions
		if client == None:
			raise Exception("Client cannot be empty")
		# Make a connection to the db
		db = pymysql.connect(self.connection,
												self.user,
												self.password,
												self.databaseName)
		cursor = db.cursor()
		# Prepare sql
		sql = "UPDATE {} SET {}={} ".format(self.CLIENTS_TABLE,
																				self.KEY_STATUS_CLIENTS,
																				client.property_status)\
					+ " WHERE {}={};".format(self.KEY_ID_CLIENTS,
																	client.property_client_id)
		try:
			# Execute sql command
			cursor.execute(sql)
			# Commit changes to db
			db.commit()
		except:
			# Rollback in case there is an error
			db.rollback()
		# Close db connection
		db.close()

	def deleteClientByID(self, client_id = None):
		# Assertions
		if client_id == None:
			raise Exception("Client id cannot be empty")
		# Make a connection to the db
		db = pymysql.connect(self.connection,
												self.user,
												self.password,
												self.databaseName)
		cursor = db.cursor()
		# Prepare sql
		sql = "DELETE FROM {}".format(self.CLIENTS_TABLE)\
					+ " WHERE {}={};".format(self.KEY_ID_CLIENTS, client_id)
		try:
			# Execute sql command
			cursor.execute(sql)
			# Commit changes to db
			db.commit()
		except:
			# Rollback in case there is an error
			db.rollback()
		# Close db connection
		db.close()

	# results
	# self.RESULTS_TABLE = "results"
	# self.KEY_ID_RESULTS = "client_id"
	# self.KEY_MICROORGANISM_RESULTS = "microorganism"
	# self.KEY_COUNT_RESULTS = "count"
		
	# CRUD operations for results
	def createResult(self, result = None):
		# Assertions
		if result == None:
			raise Exception("Result cannot be empty")
		# Make a connection to the db
		db = pymysql.connect(self.connection,
												self.user,
												self.password,
												self.databaseName)
		cursor = db.cursor()	
		# Prepare sql
		sql = "INSERT INTO {}({}, {}, {})".format(self.RESULTS_TABLE,
																							self.KEY_ID_RESULTS,
																							self.KEY_MICROORGANISM_RESULTS,
																							self.KEY_COUNT_RESULTS)\
					+ " VALUES({},'{}',{});".format(result.property_client_id,
																			result.property_microorganism,
																			result.property_count)
		print(sql)
		try:
			# Execute sql command
			cursor.execute(sql)
			# Commit changes to db
			db.commit()
		except Exception as e:
			# Rollback in case there is an error
			db.rollback()
		# Close db connection
		db.close()

	def readResults(self):
		# Local variables
		listResults = []
		# Make a connection to the db
		db = pymysql.connect(self.connection,
												self.user,
												self.password,
												self.databaseName)
		# Create a cursor
		cursor = db.cursor()
		# SQL query
		sql = "SELECT * FROM {};".format(self.RESULTS_TABLE)
		try:
			# Execute sql
			cursor.execute(sql)
			# Fetch results
			results = cursor.fetchall()
			# Append results to a list of Results
			for result in results:
				listResults.append(Result(client_id = result[1],
																	microorganism = result[2],
																	count = result[3]))
		except:
			print("Unable to fetch data")
		# Close database
		db.close()
		# Return results
		return listResults

	def readResultByID(self, client_id = None):
		# Local variables
		listResults = []
		# Assertions
		if client_id == None:
			raise Exception("Client id cannot be empty")
		# Make a connection to the db
		db = pymysql.connect(self.connection,
												self.user,
												self.password,
												self.databaseName)
		# Create a cursor
		cursor = db.cursor()
		# Create query
		sql = "SELECT * FROM {}".format(self.RESULTS_TABLE)\
					+ " WHERE {}={};".format(self.KEY_ID_RESULTS, client_id)
		try:
			# Execute sql
			cursor.execute(sql)
			# Fetch results
			results = cursor.fetchall()
			# Append results to a list of results
			for result in results:
				listResults.append(Result(client_id = result[1],
																	microorganism = result[2],
																	count = result[3]))
		except:
			print("Unable to fetch data")
		# Close connection to database
		db.close()
		# Return results
		return listResults

	def readResultByIDAndMic(self, client_id, mic):
		# Local variables
		listResults = []
		# Make a connection to db
		db = pymysql.connect(self.connection,
												self.user,
												self.password,
												self.databaseName)
		# Create a cursor
		cursor = db.cursor()
		# Create query
		sql = "SELECT * FROM {}".format(self.RESULTS_TABLE)\
					+ " WHERE {}={} and {}={};".format(self.KEY_ID_RESULTS,
																						client_id,
																						self.KEY_MICROORGANISM_RESULTS,
																						mic)
		try:
			# Execute sql
			cursor.execute(sql)
			# Fetch results
			results = cursor.fetchall()
			# Append results to a list of Results
			for result in results:
				listResults.append(Result(client_id = result.property_client_id,
																	microorganism = result.property_microorganism,
																	count = result.property_count))
		except:
			print("Unable to fetch values")
		# Close db
		db.close()
		# Return results
		return listResults

	def updateResult(self):
		# Update does not make sense
		return None

	def deleteResultsByID(self, client_id = None):
		# Assertions
		if client_id == None:
			raise Exception("Client id cannot be empty")
		# Make a connection to the db
		db = pymysql.connect(self.connection,
												self.user,
												self.password,
												self.databaseName)
		cursor = db.cursor()
		# Prepare sql
		sql = "DELETE FROM {}".format(self.RESULTS_TABLE)\
					+ " WHERE {}={};".format(self.KEY_ID_RESULTS, client_id)
		try:
			# Execute sql command
			cursor.execute(sql)
			# Commit changes to db
			db.commit()
		except:
			# Rollback in case there is an error
			db.rollback()
		# Close db connection
		db.close()

	# CRUD operations for the microorganisms table
	def createMicroorganism(self):
		# Does not make sense, this will be a static table
		pass

	def readMicroorganismByID(self, id_):
		# Local variable
		mic = Microorganism()
		# Make a connection to the db
		db = pymysql.connect(self.connection,
												self.user,
												self.password,
												self.databaseName)
		cursor = db.cursor()
		# Prepare sql
		sql = "SELECT * FROM {}".format(self.MICROORGANISMS_TABLE)\
					+ " WHERE {}={};".format(self.KEY_ID_MICROORGANISMS, id_)
		try:
			# Execute sql command
			cursor.execute(sql)
			# Fetch results
			results = cursor.fetchall()[0]
			# Load results into class
			mic.property_id = results[0]
			mic.property_name = results[1]
		except:
			print("Unable to fetch results")
		# Close db connection
		db.close()
		# Return result
		return mic

	def updateMicroorganism(self):
		# This does not make sense
		pass

	def deleteMicroorganism(self):
		# There is no point in deleting a field
		pass

if __name__ == "__main__":
	pass

# from ClientsDatabaseHandler import *
# from Client import Client
# cdb = ClientsDatabaseHandler(user = "root", password = "root")
# cdb.readClientsByStatus(status=0)
# cdb.createClient(Client(client_id=134679, status=0))

# import pymysql
# db = pymysql.connect("localhost","root","root","labomaticClients")
# cursor = db.cursor()
