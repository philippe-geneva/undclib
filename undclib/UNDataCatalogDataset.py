#
#
#

class UNDataCatalogDataset(object):
	"""
	Dataset class
	"""

	_Attributes = {}
#
#
#
	def __init__(self):
		"""
		New datasets are initialized with all of the required attributes set to 
		None, 0, or other appropriate default value.
		"""
		self._Attributes = {
			'published': None,
       			'title': None,
	 		'id_agency': None,
			'description': None,
			'additional_info': None,
			'organization': None,
			'publisher': None,
			'access_level': None,
			'publisher_clearance': None,
			'rights': None,
			'frequency': None,
			'format': None,
			'language': None,
			'data_quality': None,
			'dataset_type': None,
			'contact_type': None,
			'data_standard': None,
			'conforms_to': None,
			'described_by': None,
			'spatial_coverage': None,
			'location': None,
			'duty_station': None,
			'granularity': None,
			'tags': None,
			'sdg': None,
			'license': None,
			'temporal_coverage': None,
			'download_url': None,
			'landing_page': None,
			'contact_name': None,
			'contact_email': None,
			'contact_address': None,
			'release_date': None,
			'modified_date': None
		}
#
#
#
	def set_attribute(self,attr,value,add = None):
		"""
		Set an attribute for the dataset.  
		If you do not specify the optional parameter add, or you
		set it to False, the method will fail if you attempt to add 
		an attribute that is not part of the UN Data Catalog schema.  
		If add is set to True, the attribute will be added to the 
		dataset even if it is not part of the schema.
		
		"""
		if (add is None):
			add = False 
		if (attr is None):
			raise ValueError("You must specify an attribute")
		if (value is None):
			raise ValueError("You must specify a value")
		if ((not add) and (attr not in self._Attributes)):
			raise ValueError("Attribute " + attr + " unrecognized")
		self._Attributes[attr] = value
#
#
#
	def get_attribute(self,attr):
		"""
		Retrieve an attribute for the dataset.
		"""
		if (attr is None):
			raise ValueError("You must specify an attribute")
		if (attr not in self._Attributes):
			raise ValueError("Attribute " + attr + " unrecognized")
		return self._Attributes[attr]	
