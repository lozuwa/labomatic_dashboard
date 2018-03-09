import os
import sys

class Microorganism(object):
	"""docstring for Microorganism"""
	def __init__(self, 
								id_ = None,
								name = None):
		super(Microorganism, self).__init__()
		# This is where we define multiple constructors
		self.id_ = id_
		self.name = name
		
	@property
	def property_id(self):
		return self.id_

	@property_id.setter
	def property_id(self, id_):
		self.id_ = id_

	@property
	def property_name(self):
		return self.name

	@property_name.setter
	def property_name(self, name):
		self.name = name

