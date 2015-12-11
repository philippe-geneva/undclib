#
#
#

class UNDataCatalogError(Exception):
	"""
	Exception class for errors that are specific to the UN Data Catalog.
	"""

	def __init__(self,msg):
		self.msg = msg 
