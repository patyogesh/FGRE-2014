import xmlrpclib

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# RPC 

proxy = xmlrpclib.Server('http://localhost:8081', allow_none=True)
try:
	proxy.set_exit_choice(get_exit_choice(proxy.get_delays()))

except Exception, err:
    print 'Fault code:', err.faultCode
    print 'Message   :', err.faultString


def get_exit_choice(tup):
	if(tup[0]<tup[1]):
		return 'left'
	else:
		return 'right'