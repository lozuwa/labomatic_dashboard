"""
Client table structure.
------------
	FIELDS
------------
id_: int that defines a position in the db.
client_id: unique name that describes the client.
status: int that might have 3 states.
------------
		DESC
------------
status:
0 -> not diagnosed
1 -> working
2 -> diagnosed
"""

class Client(object):
	"""docstring for Clients"""
	def __init__(self,
							id_ = None,
							client_id = None,
							status = None):
		super(Client, self).__init__()
		# Here we define different types of constructors			
		self.id = id_
		self.client_id = client_id
		self.status = status

	# Setters and getters
	@property
	def property_id_(self):
		return self.id

	@property_id_.setter
	def property_id_(self, id_):
		self.id = id_

	@property
	def property_client_id(self):
		return self.client_id

	@property_client_id.setter
	def property_client_id(self, client_id):
		self.client_id = client_id

	@property
	def property_status(self):
		return self.status

	@property_status.setter
	def property_status(self, status):
		self.status = status

		