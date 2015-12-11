#
# Global Health Observatory
#
# Python module that implements the UN Data Catalog API for 
# submitting data set descriptions
#

import httplib
import urllib
import json
from UNDataCatalogError import UNDataCatalogError
from UNDataCatalogDataset import UNDataCatalogDataset

#
#
#

class UNDataCatalogConnector(object):
	"""
	UNDataCatalogConnector

	Connects to the UN Data Catalog web API to register and manipulate 
	data set definitions.  Errors resulting from the incorrect specification 
	of parameters to the API will result in a UNDataCatalogError exception.
	"""
	_UNDataCatalog_Host = "api-dev.undatacatalog.org"
	_UNDataCatalog_Port = 443	
	_Proxy_Host = None
	_Proxy_Port = None
	_Username = None
	_Password = None
	_API = None
	_Token = None

	def __init__(self,username,password):
		self.set_username(username)
		self.set_password(password)

#
#
#

	def set_username(self,username):
		"""
		Set the account username for connecting to the UN Data Catalog API
		If the password is changed, the cached api and token codes will be
		deleted and regenerated when needed.
		"""
		if (username is None):
			raise ValueError("You must specify a username")
		self._Username = username
		self._API = None
		self._Token = None
#
#
#
	
	def set_password(self,password):
		"""
		Set the account password for connecting to the UN Data Catalog API
		If the password is changed, the cached api and token codes will be
		deleted and regenerated when needed.
		"""
		if (password is None):
			raise ValueError("You must specify a password")
		self._Password = password
		self._API = None
		self._Token = None
#
#
#

	def set_proxy(self,host,port):
		"""
		Set an HTTP proxy server host and port.  Once set, all UN Data Catalog 
		connections will go through this proxy.
		"""
		if (host is None):
			raise ValueError("You must specify a value for the proxy host")
		if (port is None):
			raise ValueError("You must specify a value for the proxy port")
		self._Proxy_Host = host
		self._Proxy_Port = port

#
#
#

	def remove_proxy(self):
		"""
		Removes the HTTP proxy settings.
		"""
		self._Proxy_Host = None
		self._Proxy_Port = None

#
#
#

	def send_request(self,request,body = None):
		conn = None
		method = "GET"
		if (body is not None):
			method = "POST"
		print method + " " + request
		print body
		if (self._Proxy_Host is not None):
			conn = httplib.HTTPConnection(self._Proxy_Host,self._Proxy_Port)
			conn.request(method,"https://" + self._UNDataCatalog_Host + request,body);
		else:
			conn = httplib.HTTPSConnection(self._UNDataCatalog_Host,self._UNDataCatalog_Port)
			conn.request(method,request,body)
		response = conn.getresponse()
		js = json.load(response)
#
#	Internet access at WHO is forced through several proxies, so instead of 
#	assuming that we can reliably keep a connection alive in our environment, 
#	the code instead assumes that it cant, and will therefore destroy the token
#	after each use.  A fresh token will therefore be requested for each API call

		conn.close()
		self._Token = None
		error = str(js['error'])
		if (error != "0"):
			raise UNDataCatalogError(error)
		return js
#
#
#
	
	def api(self):
		"""
		Return the api code for the current username and password.
		"""
		if (self._API is None):
        		request = "/0.4/get_api?username=" + self._Username + "&password=" + self._Password
			js = self.send_request(request)
			self._API = str(js['api'])
			self._Token = None
		return self._API

#
#
#

	def token(self):
		"""
		Return the token for the current session.
		"""
		if (self._Token is None):
			request = "/0.4/get_token?api_key=" + self.api()
			js = self.send_request(request)
			self._Token = str(js['token'])
		return self._Token
		
#
#
#
	def vocabularies(self):
		"""
		Return the set of vocabularies available in the UN Data Catalog.
		Returns a set object.
		"""
		request = "/0.4/get_vocabularies"
		js = self.send_request(request)
		return set(js['vocabularies'])

#
#
#
	def terms(self,vocabulary):
		"""
		Return the set of terms associated with the specified vocabulary.
		Returns a set object.
		"""
		if (vocabulary is None):
			raise ValueError("You must specify a vocabulary")
		request = "/0.4/get_terms?vocabulary=" + vocabulary
		js = self.send_request(request)
		return set(js[vocabulary])
#
#
#
	def dataset_by_id(self,id):
		"""
		Retrieve a specific data set using its agency assigned ID
		"""
		if (id is None):
			raise ValueError("You must specify an id")
		request = "/0.4/get_dataset?id_agency=" + id
		js = self.send_request(request)
		dataset = UNDataCatalogDataset()
		attributes = js['dataset']
		for attr in attributes:
			if (attributes[attr]):
				dataset.set_attribute(attr,attributes[attr]);
		return dataset
#
#
#
	def datasets_by_organization(self,organization,published = None):
		"""
		Returns the collection of datasets published by the specified
		organization.  If the boolean parameter published is not specified, 
		then the method will return the published datasets.
		"""
		if (organization is None):
			raise ValueError("You must specify an organization")
		if (published not in (None, True, False)):
			raise ValueError("If specified, you must set published to True or False")
		if (published is None):
			published = True;	
		request = ("/0.4/dataset_get_by_organization?organization=" + organization + 
			   "&published=" + ("1" if published else "0") )
		js = self.send_request(request)
		datasets = set()
		for ds in js['datasets']:
			dataset = UNDataCatalogDataset()
			for attr in ds:
				if (ds[attr]):
					dataset.set_attribute(attr,ds[attr])
			datasets.add(dataset)
		return datasets
#
#
#
	def create(self,dataset):
		"""
		Create the provided dataset in the UN Data Catalogue
		"""
		if (dataset is None):
			raise ValueError("You must specify a UNDataCatalogDataset object")
		request = "/0.4/dataset_create?token=" + self.token() + "&username=" + self._Username
#
#		We create a special copy of the dataset's attributes where
#		we remove anything that has a None value so as not to create empty
#		attributes in the UN Data Catalog.
#
		attributes = { key:dataset._Attributes[key] 
			       for key in dataset._Attributes 
			       if dataset._Attributes[key] is not None }
		request += "&" + urllib.urlencode(attributes)
		js = self.send_request(request)
#
#
#
	def update_field(self,id_agency,field,value):
		"""
		Update the a specific field for a specific dataset description
		directly in the UN Data Catalog
		"""
		if (id_agency is None):
			raise ValueError("You must specify an id_agency")
		if (field is None):
			raise ValueError("You must specify a field")
		if (value is None):
			raise ValueError("You must specify a value")
		request = "/0.4/dataset_update_field?token=" + self.token() + "&username=" + self._Username
		params = { "agency_identifier": id_agency,
			   "field": field,
			   "value": value 
			 }
		body = urllib.urlencode(params)
		request += "&" + body
		js = self.send_request(request)
#
#
#
#	def update(self,dataset):
#		"""
#		Update a dataset entry in the UN Data Catalog using the 
#		provided entry
#		"""
#		if (dataset is None):
#			raise ValueError("You must specify a UNDataCatalogDataset object")
#		id_agency = dataset.get_attribute("id_agency")
#		if (id_agency is None):
#			raise ValueError("Dataset does not have an id_agency attribute")
#		undc_dataset = self.dataset_by_id(id_agency)
#		for attr in dataset._Attributes:
##			if (attr not in undc.dataset._Attributes):
