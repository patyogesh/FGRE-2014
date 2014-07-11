import xmlrpclib

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# RPC 

proxy = xmlrpclib.Server('http://localhost:8081', allow_none=True)
try:
	print proxy.get_delays()

except Exception, err:
    print 'Fault code:', err.faultCode
    print 'Message   :', err.faultString