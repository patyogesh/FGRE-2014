FGRE-2014-Inter-Domain-Routing-using-SDN-Controller
===================================================

##Requirements:

The following assume a Linux machine on which both the SDN controller and mininet are run.

- Install pyretic from https://github.com/frenetic-lang/pyretic
- Install mininet from https://github.com/mininet/mininet
- Copy the pyretic-reroute.py to the pyretic directory under pyretic/examples

##Running:

- Start the mininet topology

```
sudo python fgre_net_topo.py
```

- Then, start the pyretic controller with the reroute application

```
./pyretic.py -m p0 pyretic.examples.pyretic_reroute
```

- Once pyretic has started, a CLI takes over offering three choices: (r)eroute, (s)ee, and (q)uit

```
laurent-laptop:pyretic lvanbever$ ./pyretic.py pyretic.examples.pyretic_reroute
Initializing reroute policy
(r)eroute, (s)ee, or (q)uit? s
Current policy being implemented is going to left: parallel:
    sequential:
        match: ('switch', 1) ('dstip', 20.0.0.0/16) ('inport', 2)
        modify: ('dstmac', 66:66:66:66:66:aa) ('srcmac', 00:0a:aa:bb:cc:da)
        fwd 3
    sequential:
        match: ('switch', 5) ('dstip', 20.0.0.0/16) ('inport', 2)
        modify: ('dstmac', 66:66:66:66:66:ab) ('srcmac', 00:0a:aa:bb:cc:db)
        fwd 3
    sequential:
        match: ('switch', 1) ('dstip', 30.0.100.0/24) ('inport', 3)
        modify: ('dstmac', 66:66:66:66:66:ac) ('srcmac', 00:0a:aa:bb:cc:dc)
        fwd 2
    sequential:
        match: ('switch', 5) ('dstip', 30.0.100.0/24) ('inport', 3)
        modify: ('dstmac', 66:66:66:66:66:ac) ('srcmac', 00:0a:aa:bb:cc:dc)
        fwd 2
    sequential:
        match: ('switch', 2) ('dstip', 30.0.100.0/24)
        fwd 1
    sequential:
        match: ('switch', 3) ('dstip', 30.0.100.0/24)
        fwd 1
    sequential:
        match: ('switch', 4) ('dstip', 30.0.100.0/24)
        fwd 2
    sequential:
        match: ('switch', 2) ('dstip', 20.0.0.0/16)
        fwd 2
(r)eroute, (s)ee, or (q)uit?
```

The Pyretic controller should also receive measurements coming from the two measurements stations mh1 and mh2

```
...
Controller. New delay for left exit point is: 315.00
10.0.0.1 - - [26/Aug/2014 17:49:23] "POST /RPC2 HTTP/1.1" 200 -
Controller. New delay for right exit point is: 393.00
10.0.0.2 - - [26/Aug/2014 17:49:28] "POST /RPC2 HTTP/1.1" 200 -
Controller. New delay for left exit point is: 237.00
10.0.0.1 - - [26/Aug/2014 17:49:34] "POST /RPC2 HTTP/1.1" 200 -
Controller. New delay for right exit point is: 312.00
10.0.0.2 - - [26/Aug/2014 17:49:40] "POST /RPC2 HTTP/1.1" 200 -
Controller. New delay for left exit point is: 219.00
10.0.0.1 - - [26/Aug/2014 17:49:46] "POST /RPC2 HTTP/1.1" 200 -
Controller. New delay for right exit point is: 241.00
10.0.0.2 - - [26/Aug/2014 17:49:52] "POST /RPC2 HTTP/1.1" 200 -
Controller. New delay for left exit point is: 223.00
10.0.0.1 - - [26/Aug/2014 17:49:57] "POST /RPC2 HTTP/1.1" 200 -
...
```

By default, traffic from the client to the ISP is going via the left exit point. The delay on that link has been artificially increased (see the mininet configuration for how to do that). To measure latency, you can use ping in mininet directly.

```
...
mininet> client ping 20.0.0.1
PING 20.0.0.1 (20.0.0.1) 56(84) bytes of data.
64 bytes from 20.0.0.1: icmp_req=1 ttl=64 time=111 ms
64 bytes from 20.0.0.1: icmp_req=2 ttl=64 time=113 ms
64 bytes from 20.0.0.1: icmp_req=3 ttl=64 time=128 ms
64 bytes from 20.0.0.1: icmp_req=4 ttl=64 time=110 ms
64 bytes from 20.0.0.1: icmp_req=5 ttl=64 time=111 ms
...
```

As the latency on the right exit point is lower, rerouting the traffic to it will improve the RTT. To do that, just press "r" in the controller window, and then enter "right":

```
...
Invalid option
(r)eroute, (s)ee, or (q)uit? r
enter "left" or "right" right
...
```

Once this is done, the controller automatically reroute the flow to the right exit point. This has for effect to reduce the RTT betweent the client and the ISP. You can check the output of mininet for that:

```
64 bytes from 20.0.0.1: icmp_req=191 ttl=64 time=111 ms
64 bytes from 20.0.0.1: icmp_req=192 ttl=64 time=111 ms
64 bytes from 20.0.0.1: icmp_req=193 ttl=64 time=120 ms
64 bytes from 20.0.0.1: icmp_req=194 ttl=64 time=139 ms
64 bytes from 20.0.0.1: icmp_req=195 ttl=64 time=120 ms
64 bytes from 20.0.0.1: icmp_req=196 ttl=64 time=36.0 ms
64 bytes from 20.0.0.1: icmp_req=197 ttl=64 time=13.0 ms
64 bytes from 20.0.0.1: icmp_req=198 ttl=64 time=13.1 ms
64 bytes from 20.0.0.1: icmp_req=199 ttl=64 time=13.5 ms
64 bytes from 20.0.0.1: icmp_req=200 ttl=64 time=13.1 ms
```

Similarly, rerouting the traffic to the left will increase the RTT:

##TODO:

- The controller should normally reroute the flows by itself based on the measurements, currently this is done manually.
