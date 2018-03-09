import os
import sys

class Result(object):
	"""docstring for Result"""
	def __init__(self, 
							id_ = None,
							client_id = None,
							microorganism = None,
							count = None):
		super(Result, self).__init__()
		# Define multiple constructors
		self.id_ = id_
		self.client_id = client_id
		self.microorganism = microorganism
		self.count = count

	@property
	def property_id(self):
		return self.id_

	@property_id.setter
	def property_id(self, id_):
		self.id_ = id_

	@property
	def property_client_id(self):
		return self.client_id

	@property_client_id.setter
	def property_client_id(self, client_id):
		self.client_id = client_id

	@property
	def property_microorganism(self):
		return self.microorganism

	@property_microorganism.setter
	def property_microorganism(self, microorganism):
		self.microorganism = microorganism
		
	@property
	def property_count(self):
		return self.count

	@property_count.setter
	def property_count(self, count):
		self.count = count

		

