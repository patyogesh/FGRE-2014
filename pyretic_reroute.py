#######################################################
#
# FGRE 2014, Interdomain reroute flow application
#
#######################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.modules.mac_learner import mac_learner
import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer

#########################
##
## IP Prefixes
##
#########################

ISP_prefix = IPPrefix('20.0.0.0/16')
CLIENT_prefix = IPPrefix('30.0.100.0/24')

#########################
##
## MAC addresses
##
#########################

MAC_ISP = MAC('66:66:66:66:66:aa')
MAC_CLIENT = MAC('66:66:66:66:66:ac')

MAC_isp_gw = MAC('00:0a:aa:bb:cc:da')
MAC_client_gw = MAC('00:0a:aa:bb:cc:dc')

#########################
##
## Switch Port IDs
##
#########################

SWITCH1_PORT_MH1 = 1
SWITCH1_PORT_SWITCH2 = 2
SWITCH1_EXTERNAL_PORT = 3

SWITCH2_PORT_CLIENT = 1
SWITCH2_PORT_SWITCH1 = 2
SWITCH2_PORT_SWITCH3 = 3
SWITCH2_PORT_SWITCH4 = 4

SWITCH3_PORT_SWITCH2 = 1
SWITCH3_PORT_SWITCH4 = 2
SWITCH3_PORT_SWITCH5 = 3

SWITCH4_PORT_SWITCH2 = 2
SWITCH4_PORT_SWITCH3 = 1

SWITCH5_PORT_MH2 = 1
SWITCH5_PORT_SWITCH3 = 2
SWITCH5_EXTERNAL_PORT = 3

SWITCH6_PORT_ISP = 3
SWITCH6_PORT_SWITCH1 = 1
SWITCH6_PORT_SWITCH5 = 2

###############################
##
##  default pyretic policies
##
###############################

infrastructure_routing_policy = (
	(match(dstip=ISP_prefix, inport=SWITCH1_PORT_SWITCH2, switch=1) >> modify(srcmac=MAC_isp_gw, dstmac=MAC_ISP) >> fwd(SWITCH1_EXTERNAL_PORT)) +
	(match(dstip=ISP_prefix, inport=SWITCH5_PORT_SWITCH3, switch=5) >> modify(srcmac=MAC_isp_gw, dstmac=MAC_ISP) >> fwd(SWITCH5_EXTERNAL_PORT)) +

	(match(dstip=CLIENT_prefix, inport=SWITCH1_EXTERNAL_PORT, switch=1) >> modify(srcmac=MAC_client_gw, dstmac=MAC_CLIENT) >> fwd(SWITCH1_PORT_SWITCH2)) +
	(match(dstip=CLIENT_prefix, inport=SWITCH5_EXTERNAL_PORT, switch=5) >> modify(srcmac=MAC_client_gw, dstmac=MAC_CLIENT) >> fwd(SWITCH5_PORT_SWITCH3)) +
	
	(match(dstip=CLIENT_prefix, switch=2) >> fwd(SWITCH2_PORT_CLIENT)) +
	(match(dstip=CLIENT_prefix, switch=3) >> fwd(SWITCH3_PORT_SWITCH2)) +
	(match(dstip=CLIENT_prefix, switch=4) >> fwd(SWITCH4_PORT_SWITCH2)) +
	
	(match(dstmac=MAC('66:66:66:66:66:aa'), srcmac=MAC('ce:f4:8d:6a:d4:21'), inport=SWITCH1_PORT_MH1, switch=1) >> fwd(SWITCH1_EXTERNAL_PORT)) +
	(match(srcmac=MAC('66:66:66:66:66:aa'), dstmac=MAC('ce:f4:8d:6a:d4:21'), inport=SWITCH1_EXTERNAL_PORT, switch=1) >> fwd(SWITCH1_PORT_MH1)) +
	
	(match(dstmac=MAC('66:66:66:66:66:aa'), srcmac=MAC('de:70:85:4b:9b:11'), inport=SWITCH5_PORT_MH2, switch=5) >> fwd(SWITCH5_EXTERNAL_PORT)) +
	(match(srcmac=MAC('66:66:66:66:66:aa'), dstmac=MAC('de:70:85:4b:9b:11'), inport=SWITCH5_EXTERNAL_PORT, switch=5) >> fwd(SWITCH5_PORT_MH2)) +
	
	(match(dstip=ISP_prefix, switch=6) >> fwd(SWITCH6_PORT_ISP)) +
	(match(dstip=CLIENT_prefix, switch=6) >> fwd(SWITCH6_PORT_SWITCH5))
)

to_ISP_left = (
	(match(dstip=ISP_prefix, switch=2) >> fwd(SWITCH2_PORT_SWITCH1))
)

to_ISP_right = (
	(match(dstip=ISP_prefix, switch=2) >> fwd(SWITCH2_PORT_SWITCH3)) +
	(match(dstip=ISP_prefix, switch=3) >> fwd(SWITCH3_PORT_SWITCH5))
)


class DelayHandler:
	
	def __init__(self, policy):
		self.delay_left = 0.00
		self.delay_right = 0.00
		self.current_choice = "left"
		self.policy = policy
		self.counter = 0
	
	def update_decision(self):
		if self.delay_left < self.delay_right:
			if self.current_choice != "left":
				self.current_choice = "left"
				self.set_exit_choice("left")
			else:
				print "Controller. Updating path. left one is still better than the right one. Not moving."
		else:
			if self.current_choice != "right":
				self.current_choice = "right"
				self.set_exit_choice("right")
			else:
				print "Controller. Updating path. right one is still better than the right one. Not moving."
	
	def set_left_delay(self, val):
		self.delay_left = val
		self.counter += 1
		print "Controller. New delay for left exit point is: %.2f" % (val)
		if (self.counter % 10 == 0):
			self.update_decision()
		return True

	def set_right_delay(self, val):
		self.delay_right = val
		self.counter += 1
		print "Controller. New delay for right exit point is: %.2f" % (val)
		if (self.counter % 10 == 0):
			self.update_decision()
		return True

	def set_exit_choice(self, val):
		if val == "left" or val == "right":
			self.policy.update_policy(val)
		else:
			pass
		return True

	def get_delays(self):
		return (self.delay_left, self.delay_right)


class ServerThread(threading.Thread):
	def __init__(self,policy):
		threading.Thread.__init__(self)
		self.localServer = SimpleXMLRPCServer(('0.0.0.0', 8081), allow_none=True)
		self.localServer.register_instance(DelayHandler(policy))

	def run(self):
		self.localServer.serve_forever()

class reroute_interdomain(DynamicPolicy):
	
	def __init__(self):
		print "Initializing reroute policy"
		super(reroute_interdomain,self).__init__(identity)
		
		server = ServerThread(self)
		server.start()
		
		self.policy = infrastructure_routing_policy + to_ISP_left

		self.ui = threading.Thread(target=self.ui_loop)
		self.ui.daemon = True
		self.ui.start()
		
	def update_policy (self, direction="left"):
		print "Controller. Updating exit policy to %s. Current policy was %s" % (direction, self.direction)
		if direction == "left":
			self.direction = "left"
			self.policy = infrastructure_routing_policy + to_ISP_left
		else:
			self.direction = "right"
			self.policy = infrastructure_routing_policy + to_ISP_right
	
	def ui_loop(self):
		while(True):
			nb = raw_input('(r)eroute, (s)ee, or (q)uit? ')
			if nb == 'r':
				nb = raw_input('enter "left" or "right" ')
				if nb == "left":
					self.update_policy("left")
				elif nb == "right":
					self.update_policy("right")
				else:
					print 'Incorrect direction. Correct directions are "left" or "right" '
			elif nb == 's':
				print "Current policy being implemented is going to %s: %s" % (self.direction, self.policy)
			elif nb == 'q':
				print "Quitting"
				import os, signal
				os.kill(os.getpid(), signal.SIGINT)
				return
			else:
				print "Invalid option"

def main ():
	return if_(
			(match(dstip=ISP_prefix) | match(dstip=CLIENT_prefix)),
			reroute_interdomain(),
			mac_learner()
		)