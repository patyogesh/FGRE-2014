import xmlrpclib

proxy = xmlrpclib.Server('http://localhost:8081', allow_none=True)
try:
    print proxy.disp_msg('Hello')
except Exception, err:
    print 'Fault code:', err.faultCode
    print 'Message   :', err.faultString

