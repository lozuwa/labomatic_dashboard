# Mysql
import pymysql

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
		self.CLIENTS_TABLE = "clients"
		self.KEY_ID = "client_id"
		self.KEY_STATUS = "status"

	# CRUD operations
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
																					self.KEY_ID,
																					self.KEY_STATUS)\
					+	" VALUES({}, {});".format(client.property_client_id,
																				client.property_status)
		print("SQL: ", sql)
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
		# Make a connection to the db
		db = pymysql.connect(self.connection,
												self.user,
												self.password,
												self.databaseName)
		cursor = db.cursor()
		# Prepare sql
		sql = "SELECT * FROM {};".format(self.CLIENTS_TABLE)
		print("SQL: ", sql)
		try:
			# Execute sql
			cursor.execute(sql)
			# Fetch all rows in a list of lists
			results = cursor.fetchall()
		except:
			print("Unable to fetch data")
		# Close db connection
		db.close()
		# Return
		return results

	def readClientByID(self, client_id = None):
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
						+ " WHERE {}={};".format(self.KEY_ID, client_id)
		print("SQL: ", sql)
		try:
			# Execute sql
			cursor.execute(sql)
			# Fetch all rows in a list of lists
			results = cursor.fetchall()
		except:
			print("Unable to fetch data")
		# Close db connection
		db.close()
		# Return
		return results

	def readClientsByStatus(self, status = None):
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
						+ " WHERE {}={};".format(self.KEY_STATUS,
																		status)
		print("SQL: ", sql)
		try:
			# Execute sql
			cursor.execute(sql)
			# Fetch all rows in a list of lists
			results = cursor.fetchall()
		except:
			print("Unable to fetch data")
		# Close db connection
		db.close()
		# Return
		return results

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
																				self.KEY_STATUS,
																				client.property_status)\
					+ " WHERE {}={};".format(self.KEY_ID,
																	client.property_client_id)
		try:
			# Execute sql command
			cursor.execute(sql)
			# Commit changes to db
			db.commit()
		except:
			# Rollback in case there is an error
			db.Rollback()
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
					+ " WHERE {}={};".format(self.KEY_ID, client_id)
		try:
			# Execute sql command
			cursor.execute(sql)
			# Commit changes to db
			db.commit()
		except:
			# Rollback in case there is an error
			db.Rollback()
		# Close db connection
		db.close()

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
