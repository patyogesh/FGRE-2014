#!/bin/bash
rtt=1
Delay=500ms
PingCount=5
IP1=192.168.0.110
####################################
#	HOST -1
#
# Try to induce delay randomly
# Here for any random number 7 < n < 10
# induce delay of $Delay ms
#
####################################

rand1=($(shuf -i 0-10 -n 10))
echo "$rand1"

echo "Initial Delay----"
fping -e -q  $IP1 -c $PingCount 2> out.txt
cat out.txt | awk '{print $1" "$5" "$8}' | sed 's/\// /g' | sed 's/\%,/ /g' > host1.txt

if [ $rand1 -gt 7 ] ;then
	echo "After Inducing Delay of $Delay----"
	sudo tc qdisc add dev wlan0 root netem delay $Delay
fi

sudo tc qdisc del dev wlan0 root netem
