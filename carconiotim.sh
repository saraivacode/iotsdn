#!/bin/bash

#control flag
flag="c0"
#Identify sta wireless interface
int=$(ifconfig | grep wlan | cut -d' ' -f1)
#Identify sta number for future reference
sta=$(ifconfig | grep wlan | cut -d' ' -f1| cut -d'-' -f1 | sed 's/sta//')
#Start tcpdump in each vehicle to capture data and analize after
tcpdump -i sta$sta\-wlan0 --direction=out -tttttnnvS --immediate-mode -l > sta$sta\.txt &
#Save start data time for future analis
t=$(date +%s.%N)
echo tempo_ini $t > logsta$sta\.txt

while [[ true ]]; do
	#If sta is connected begins transmition. Save ping output to generate RTT mean in data analisis
	if [[ $(iw dev $int link | grep SSID) != "" ]] && [[ $flag != "c1" ]]; then
		#control flag = c1 (trasmition will be initiated)
		flag="c1"
		#Save time to further analisis
		t=$(date +%s.%N)
		echo tempo_transm $t >> logsta$sta\.txt

        #Start transmission to server E2 - IM
		hping3 --udp -p 5003 -i u96000 -d 1470 10.0.2.12 -q &
		h3=$!
		ping 10.0.2.12 -i 1 -c 330 | while read line; do echo $(date +%s) - $line >> ping$sta\_h3.txt; done &
		p3=$!

	#if disconnected finalize transmission
	elif [[ $(iw dev $int link | grep SSID) = "" ]] && [[ $flag = "c1" ]]; then
		#Kill process. Finalize trnasmissions
		kill -9 $h3 $p3 
		#control flag = c0 (trasmition is stoped)
		flag="c0"
	fi
	sleep 0.5
done

