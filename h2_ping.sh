#!/bin/bash
rtt=1
Delay=500ms
PingCount=5
IP1=192.168.0.110

####################################
#	HOST -2
#
# Try to induce delay randomly
# Here for any random number 17 < n < 20
# induce delay of $Delay ms
#
####################################
rand2=($(shuf -i 10-20 -n 10))
echo "$rand2"

echo "Initial Delay----"
fping -e -q  $IP2 -c $PingCount 2> out.txt
cat out.txt | awk '{print $1" "$5" "$8}' | sed 's/\// /g' | sed 's/\%,/ /g' > host2.txt

if [ $rand2 -gt 17 ] ;then
	echo "After Inducing Delay of $Delay----"
	sudo tc qdisc add dev wlan0 root netem delay $Delay
fi

sudo tc qdisc del dev wlan0 root netem
