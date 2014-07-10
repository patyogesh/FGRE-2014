#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.util import customConstructor

def fgreTopo():
	"Create an empty network and add nodes to it."
	
	info( '*** Adding controller\n' )
	ctrlr = lambda n: RemoteController(n, ip='127.0.0.1', port=6633)
	net = Mininet(controller=ctrlr, switch=OVSKernelSwitch, autoSetMacs=False, autoStaticArp=False)
	c1 = net.addController('c1')

	info( '*** Adding hosts\n' )
	mh1 = net.addHost('mh1', ip='10.0.0.1')
	mh2 = net.addHost('mh2', ip='10.0.0.2')
	isp = net.addHost('isp')
	client = net.addHost('client')

	info( '*** Adding switch\n' )
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	s3 = net.addSwitch('s3')
	s4 = net.addSwitch('s4')
	s5 = net.addSwitch('s5')
	s6 = net.addSwitch('s6')

	info( '*** Creating links\n' )
	net.addLink(mh1, s1) # S1 port 1
	net.addLink(client, s2) # S2 port 1
	net.addLink(mh2, s5) # S5 port 1
	net.addLink(s1, s2) # S1 port 2, S2 port 2 
	net.addLink(s2, s3) # S2 port 3, S3 port 1
	net.addLink(s3, s4) # S3 port 2, S4 port 1
	net.addLink(s3, s5) # S3 port 3, S5 port 2
	net.addLink(s2, s4) # S2 port 4, S4 port 2
	net.addLink(s1, s6) # S1 port 3, S6 port 1
	net.addLink(s5, s6) # S5 port 3, S6 port 2
	net.addLink(s6, isp) # S6 port 3

	info( '*** Starting network\n')
	net.start()

	info( '*** Configuring ISP \n' )
	isp = net.get('isp')
	
	isp.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
	
	isp.cmd('ifconfig isp-eth0 down')
	isp.cmd('ifconfig isp-eth0 hw ether 66:66:66:66:66:aa up')
	isp.cmd('ifconfig isp-eth0 30.0.1.2/24 up')
	isp.cmd('ifconfig lo:1 20.0.0.1/16 up')
	
	isp.cmd('arp -s 30.0.1.1 00:0a:aa:bb:cc:da')
	isp.cmd('ip route add 30.0.0.0/16 via 30.0.1.1 dev isp-eth0')

	info( '*** Configuring Client \n' )
	client = net.get('client')
	
	client.cmd('ifconfig client-eth0 down')
	client.cmd('ifconfig client-eth0 hw ether 66:66:66:66:66:ac up')
	client.cmd('ifconfig client-eth0 30.0.100.2/24 up')
	
	client.cmd('arp -s 30.0.100.1 00:0a:aa:bb:cc:dc')
	client.cmd('ip route add 20.0.0.0/16 via 30.0.100.1 dev client-eth0')
	
	info( '*** Running CLI\n' )
	CLI(net)

	#info( '*** Running ping commands\n' )
	#host1 = net.get('mh1')
	#result1 = host1.cmd('fping -e -c 5 -i 1000 10.0.0.2')
	#print result1
    #
	#host2 = net.get('mh2')
	#result2 = host2.cmd('fping -e -c 5 -i 1000 10.0.0.1')
	#print result2

	#info( '*** Stopping network\n' )
	#net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	fgreTopo()

