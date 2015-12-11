#
# Global Health Observatory
#

import undclib

Username = "philippe.boucher"
Password = "576h83d3"
Proxy_host = "proxy05.who.int"
Proxy_port = 3128

testid = 0

#
#
#

undc = None
testid += 1
title = "Initiating UNDataCatalogConnector without parameters"
details = None
result = None
try:
	undc = undclib.UNDataCatalogConnector()
	result = "ERROR"
	details = "No exception occured, TypeError expected."
except TypeError as e:
	result = "OK"
except Exception as e:
	result = "ERROR"
	details = "Unexpected exception," + str(e)
print  ("TEST%05d" % testid) + ": " + result + ( (" (" + details + ")") if details else "")

#
#
#

undc = None
testid += 1
title = "Initiating UNDataCatalogConnection with empty username and password"
details = None
result = None
try:
	undc = undclib.UNDataCatalogConnector(None,None)
	result = "ERROR"
	details = "No exception occured, ValueError expected."
except ValueError as e:
	result = "OK"
except Exception as e:
	result = "ERROR"
	details = "Unexpected exception," + str(e)
print ("TEST%05d" % testid) + ": " + result + ( (" (" + details + ")") if details else "")

#
#
#

undc = None
testid += 1
title = "Initiating UNDataCatalogConnection with proper username and password"
details = None
result = None
try:
	undc = undclib.UNDataCatalogConnector(Username,Password)
	result = "OK"
except Exception as e:
	result = "ERROR"
	details = "Unexpected exception," + str(e)
print  ("TEST%05d" % testid) + ": " + result + ( (" (" + details + ")") if details else "")

#
#
#

undc == None
testid += 1
title = "Setting a proxy for a connection"
details = None
result = None
try:
	undc = undclib.UNDataCatalogConnector(Username,Password)
	undc.set_proxy(Proxy_host,Proxy_port)
	result = "OK"
except Exception as e:
	result = "ERROR"
	details = "Unexpected exception," + str(e)
print ("TEST%05d" % testid) + ": " + result + ( (" (" + details + ")") if details else "")

#
#
#

undc = None
testid += 1
title = "Getting an API code with a valid username and password through a proxy"
details = None
Results = None
try:
	undc = undclib.UNDataCatalogConnector(Username,Password)
	undc.set_proxy(Proxy_host,Proxy_port)
	api = undc.api();
        if (len(api) != 32):
		result = "ERROR"
		details = "api code is incorrect size"
	else:
		result = "OK"
except Exception as e:
	result = "ERROR"
	details = "Unexpected exception," + str(e)
print ("TEST%05d" % testid) + ": " + result + ( (" (" + details + ")") if details else "")

#
#
#

undc = None
testid += 1
title = "Getting an API code with an invalid username and password through a proxy"
details = None
Results = None
try:
	undc = undclib.UNDataCatalogConnector(Username + "X" ,Password)
	undc.set_proxy(Proxy_host,Proxy_port)
	api = undc.api();
	result = "ERROR"
	details = "Retrieved api code using incorrect credentials"
except undclib.UNDataCatalogError as e:
	result = "OK"
except Exception as e:
	result = "ERROR"
	details = "Unexpected exception," + str(e)
print ("TEST%05d" % testid) + ": " + result + ( (" (" + details + ")") if details else "")

#undc = undclib.UNDataCatalogConnector("philippe.boucher","576h83d3")

#undc = undclib.UNDataCatalogConnector("philippe.boucher","576h83d3")
#undc.set_proxy("proxy05.who.int",3128)
# print "API code is " + undc.api()
# print "API code is " + undc.api()
# print "My token is " + undc.token()
# print "My Token direst is " + undc._Token
# print "Vocabularies are " 
# for t in undc.vocabularies():
# 	print t 
# print ""
# print "Terms for frequenecy:"
# for t in undc.terms('frequency'):
# 	print t
#for d in undc.datasets_by_organization("UNDP"):
#	print str(d.get_attribute('id_agency')) + ", " + str(d.get_attribute('title'))
# count = 1
# for d in undc.datasets_by_organization("WHO"):
# 	print "Dataset # " + str(count)
# 	count = count + 1
# 	for a in d._Attributes:
# 		print (a,"=",d.get_attribute(a))
#dataset = undc.dataset_by_id("41114-PROJECT-00061275")
# dataset.set_attribute("publisher","Splinter can add stuff to this")
# dataset.set_attribute("format","CSV")
#for attr in dataset._Attributes:
#	if (dataset.get_attribute(attr) is not None):
#		print (attr,"=",dataset.get_attribute(attr))
#undc.create(dataset)	
#
#try:
#	undc.update_field("41114-PROJECT-00061275","publisher","Splinter changed this")
#except Exception as e:
##	print "Got some sort of exception:"
#	print e
#
#dataset = undc.dataset_by_id("41114-PROJECT-00061275")
#for attr in dataset._Attributes:
#	if (dataset.get_attribute(attr) is not None):
##		print (attr,"=",dataset.get_attribute(attr))
