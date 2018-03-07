# Mysql
import pymysql

class ResultsDatabaseHandler(object):
	"""docstring for ResultsDatabaseHandler"""
	# Constructor
	def __init__(self,
							connection = None,
							user = None,
							password = None):
		super(ResultsDatabaseHandler, self).__init__()
		# Assertions
		if connection == None:
			connection = "localhost"


		