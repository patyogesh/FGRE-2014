#!/bin/bash
rtt=1
Delay=500ms
PingCount=5
IP1=192.168.0.110
IP2=192.168.0.110
#IP1=10.10.131.80
#IP2=10.10.131.81
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

#echo "More and More bad network condition----"
#sudo tc qdisc add dev wlan0 root netem delay 200ms 40ms 25% loss 15.3% 25% duplicate 1% corrupt 0.1% reorder 5% 50%

#fping -e -q  $IP1 $IP2 -c $PingCount 2> out.txt
#cat out.txt | awk '{print $1" "$5" "$8}' | sed 's/\// /g' | sed 's/\%,/ /g' > raw_3.txt

sudo tc qdisc del dev wlan0 root netem
