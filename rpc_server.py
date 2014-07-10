from SimpleXMLRPCServer import SimpleXMLRPCServer

# server URL
server = SimpleXMLRPCServer(('localhost', 8081), allow_none=True)

# display received string
def disp_msg(message):
	print message

server.register_function(disp_msg)
try:
    print 'Use Control-C to exit'
    server.serve_forever()
except KeyboardInterrupt:
    print 'Exiting'



