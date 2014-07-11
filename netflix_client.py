import xmlrpclib

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# RPC 

proxy = xmlrpclib.Server('http://localhost:8081', allow_none=True)
try:
	proxy.set_exit_choice(min(proxy.get_delays()))

except Exception, err:
    print 'Fault code:', err.faultCode
    print 'Message   :', err.faultString