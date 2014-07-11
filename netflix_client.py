import xmlrpclib
import threading
import time

current_choice = "left"

def get_exit_choice(tup):
	if(tup[0]<tup[1]):
		return "left"
	else:
		return "right"

def update_best_exit_point():
	global current_choice
	
	while True:
		try:
			print "Fetching latest measurements from the controller..."
			current_delays = proxy.get_delays()
			print "Current delays to ISP:  (left: %.2f. right: %.2f)" % (current_delays[0], current_delays[1])
			new_choice = get_exit_choice(current_delays)
			
			if current_choice == new_choice:
				print "Current exit point (%s) is still currently the best. Not moving" % (current_choice)
			else:
				print "Other exit point (%s) is better than the current exit point. Moving" % (new_choice)
				proxy = xmlrpclib.Server('http://10.0.0.100:8081', allow_none=True)
				proxy.set_exit_choice(new_choice)
				current_choice = new_choice
		
		except Exception, err:
			print 'Fault code:', err.faultCode
			print 'Message   :', err.faultString
		time.sleep(15)

update_best_exit_point()