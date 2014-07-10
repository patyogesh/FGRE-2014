#!/bin/sh
rtt=1
Delay=500ms
PingCount=2
IP1=10.10.131.84
IP2=10.10.131.83

echo "Initial Delay----"

#fping -e -q  $IP1 $IP2 -c $PingCount -s 2> out.txt
fping -e -q  $IP1 $IP2 -c $PingCount 2> out.txt
pings=`cat out.txt | grep "xmt/rcv/%loss" | awk '{ print $5 $8}'`
echo $pings > temp.txt
awk '{ sub(/%,/,"/"); sub(/\//, " "); print($0); }' temp.txt
return

echo "After Inducing Delay of $Delay----"
sudo tc qdisc add dev wlan0 root netem delay $Delay

#fping -e -q  $IP1 $IP2 -c $PingCount -s 2> out.txt
fping -e -q  $IP1 $IP2 -c $PingCount 2> out.txt
min=`cat out.txt | grep "round trip time" | awk '{ if(NR==1) print $'$rtt' }'`
avg=`cat out.txt | grep "round trip time" | awk '{ if(NR==2) print $'$rtt' }'`
max=`cat out.txt | grep "round trip time" | awk '{ if(NR==3) print $'$rtt' }'`
echo $min
echo $avg
echo $max

#More 
#echo "More and More bad network condition----"
#sudo tc qdisc add dev wlan0 root netem delay 200ms 40ms 25% loss 15.3% 25% duplicate 1% corrupt 0.1% reorder 5% 50%

echo "Removing Delay----"
sudo tc qdisc del dev wlan0 root netem
#fping -e -q  $IP1 $IP2 -c $PingCount -s 2> out.txt
fping -e -q  $IP1 $IP2 -c $PingCount 2> out.txt
min=`cat out.txt | grep "round trip time" | awk '{ if(NR==1) print $'$rtt' }'`
avg=`cat out.txt | grep "round trip time" | awk '{ if(NR==2) print $'$rtt' }'`
max=`cat out.txt | grep "round trip time" | awk '{ if(NR==3) print $'$rtt' }'`
echo $min
echo $avg
echo $max
