from SimpleXMLRPCServer import SimpleXMLRPCServer

# server URL
server = SimpleXMLRPCServer(('localhost', 8081), allow_none=True)

class DelayHandler:
	# set delay in left branch
	def set_left_delay(self, val):
		self.delay_left = val
		print self.delay_left
		return True

	# set delay in right branch
	def set_right_delay(self, val):
		self.delay_right= val
		return True

	# set client choice
	def set_exit_choice(self, val):
		self.exit_choice = val
		return True

	# get delays
	def get_delays(self):
		delay_tup = (self.delay_left, self.delay_right)
		return delay_tup


# display received string
#def disp_msg(message):
#	print message

#server.register_function(disp_msg)

server.register_instance(DelayHandler())

try:
    print 'Use Control-C to exit'
    server.serve_forever()
except KeyboardInterrupt:
    print 'Exiting'



