import xmlrpclib
import threading
import time
import os

# get the average delay
def get_current_delay(filename):
	try:
		f = open(filename, "r")
		for line in f:
			splitted_line = line.split()
			cur_delay = float(splitted_line[5])
		f.close()
	except IndexError:
		return None
	return cur_delay

# update the link delays with current latency between links  based on ping results
def cur_ping_status():
	while True:
		print "Collecting statistics thread... Waking up"
		os.system('./h2_ping.sh')
		time.sleep(2)
		current_delay = get_current_delay("host2.txt")
		if current_delay is not None:
			print "Current average delay towards exit point is: %.2f" % (current_delay)
			
			print "Updating the controller with latest delays updates..."
			proxy = xmlrpclib.Server('http://10.0.0.100:8081', allow_none=True)
			try:
				print proxy.set_right_delay(current_delay)
			except Exception, err:
			    print 'Fault code:', err.faultCode
			    print 'Message   :', err.faultString
		else:
			print "Passing..."
		time.sleep(5)

cur_ping_status()