#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def fgreTopo():
	"Create an empty network and add nodes to it."
	net = Mininet(controller = Controller)

	info( '*** Adding controller\n' )
	ctrl = net.addController('c0')

	info( '*** Adding hosts\n' )
	mh1 = net.addHost('mh1')
	mh2 = net.addHost('mh2')
	isp = net.addHost('isp')
	client = net.addHost('client')


	info( '*** Adding switch\n' )
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	s3 = net.addSwitch('s3')
	s4 = net.addSwitch('s4')
	s5 = net.addSwitch('s5')

	info( '*** Creating links\n' )
	net.addLink(mh1, s1)
	net.addLink(client, s2)
	net.addLink(mh2, s5)
	net.addLink(s1, s2)
	net.addLink(s2, s3)
	net.addLink(s3, s4)
	net.addLink(s3, s5)
	net.addLink(s1, isp)
	net.addLink(s5, isp)
	#net.addLink(s4, ctrl)

	info( '*** Starting network\n')
	net.start()

	info( '*** Running CLI\n' )
	CLI(net)

	info( '*** Stopping network' )
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	fgreTopo()

