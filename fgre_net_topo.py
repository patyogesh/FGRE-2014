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
	mh1 = net.addHost('mh1', ip='10.0.0.1')
	mh2 = net.addHost('mh2', ip='10.0.0.2')
	isp = net.addHost('isp', ip='20.0.0.1/16')
	client = net.addHost('client', ip='30.0.0.1/24')

	info( '*** Adding switch\n' )
	s1 = net.addSwitch('s1', mac='00:00:00:00:00:01')
	s2 = net.addSwitch('s2', mac='00:00:00:00:00:02')
	s3 = net.addSwitch('s3', mac='00:00:00:00:00:03')
	s4 = net.addSwitch('s4', mac='00:00:00:00:00:04')
	s5 = net.addSwitch('s5', mac='00:00:00:00:00:05')

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

	#info( '*** Running CLI\n' )
	#CLI(net)

	info( '*** Configuring ISP \n' )
	iSrPr = net.get('isp')
	iSrPr.cmd('ifconfig lo0 20.0.0.1/16 up')
	iSrPr.cmd('ifconfig eth0 30.0.1.2/24 up')
	iSrPr.cmd('ifconfig eth1 30.0.2.2/24 up')
	iSrPr.cmd('arp -s 30.0.1.1 00:0a:aa:bb:cc:da')
	iSrPr.cmd('arp -s 30.0.2.1 00:0a:aa:bb:cc:db')
	iSrPr.cmd('ip route add 30.0.0.0/16 via 30.0.2.1 dev eth1')

	info( '*** Configuring Client \n' )
	client1 = net.get('client')
	client1.cmd('ifconfig eth0 30.0.100.2/24 up')
	client1.cmd('arp -s 30.0.100.1 00:0a:aa:bb:cc:dc')
	client1.cmd('ip route add 20.0.0.0/16 via 30.0.100.1 dev eth0')


	info( '*** Running ping commands\n' )
	host1 = net.get('mh1')
	result1 = host1.cmd('fping -e -c 5 -i 1000 10.0.0.2')
	print result1

	host2 = net.get('mh2')
	result2 = host2.cmd('fping -e -c 5 -i 1000 10.0.0.1')
	print result2

	#info( '*** Stopping network\n' )
	#net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	fgreTopo()

