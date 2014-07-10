#!/bin/sh
rtt=1
Delay=500ms
PingCount=5
IP1=10.10.131.80
IP2=10.10.131.81

echo "Initial Delay----"
fping -e -q  $IP1 $IP2 -c $PingCount 2> out.txt
cat out.txt | awk '{print $1" "$5" "$8}' | sed 's/\// /g' | sed 's/\%,/ /g' > raw.txt

#returning from here for now for simpler ingration cycle
return

echo "After Inducing Delay of $Delay----"
sudo tc qdisc add dev wlan0 root netem delay $Delay

fping -e -q  $IP1 $IP2 -c $PingCount 2> out.txt
cat out.txt | awk '{print $1" "$5" "$8}' | sed 's/\// /g' | sed 's/\%,/ /g' > raw_2.txt

sudo tc qdisc del dev wlan0 root netem

echo "More and More bad network condition----"
sudo tc qdisc add dev wlan0 root netem delay 200ms 40ms 25% loss 15.3% 25% duplicate 1% corrupt 0.1% reorder 5% 50%

fping -e -q  $IP1 $IP2 -c $PingCount 2> out.txt
cat out.txt | awk '{print $1" "$5" "$8}' | sed 's/\// /g' | sed 's/\%,/ /g' > raw_3.txt

sudo tc qdisc del dev wlan0 root netem
