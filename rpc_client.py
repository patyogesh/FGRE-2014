import xmlrpclib

proxy = xmlrpclib.Server('http://localhost:8081', allow_none=True)
try:
    #print proxy.disp_msg('Hello')
    print proxy.set_left_delay(150)
    print proxy.set_right_delay(220)
    print proxy.get_delays()

except Exception, err:
    print 'Fault code:', err.faultCode
    print 'Message   :', err.faultString

