import xmlrpclib
import threading
import time
import os

# get the average delay
def get_current_delay(filename):
	f = open(filename, "r")
	for line in f:
		splitted_line = line.split()
		cur_delay = float(splitted_line[5])
	f.close()
	return cur_delay

# update the link delays with current latency between links  based on ping results
def cur_ping_status():
	print "Collecting statistics thread... Waking up"
	os.system('./h1_ping.sh')
	time.sleep(2)
	current_delay = get_current_delay("host1.txt")
	print "Current average delay towards exit point is: %.2f" % (current_delay)
	
	print "Updating the controller with latest delays updates..."
	proxy = xmlrpclib.Server('http://10.0.0.100:8081', allow_none=True)
	try:
		print proxy.set_right_delay(current_delay)
	except Exception, err:
	    print 'Fault code:', err.faultCode
	    print 'Message   :', err.faultString

threading.Timer(5.0, cur_ping_status).start()