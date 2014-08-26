FGRE-2014-Inter-Domain-Routing-using-SDN-Controller
===================================================

##Requirements:

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
./pyretic.py pyretic.examples.pyretic_reroute
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

