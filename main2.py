#!/usr/bin/python

'Setting the position of nodes'

from mininet.node import Controller, OVSKernelSwitch
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI_wifi
from mn_wifi.node import OVSKernelAP
from mn_wifi.net import Mininet_wifi
from mininet.link import TCLink

import os
import time
import sys

def topology(flag):

    net = Mininet_wifi(controller=Controller, accessPoint=OVSKernelAP, switch=OVSKernelSwitch)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8', position='44,52,0', range=50)
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.2/8', position='45,52,0', range=50)
    sta3 = net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.3/8', position='46,52,0', range=50)
    
    sta4 = net.addStation('sta4', mac='00:00:00:00:00:05', ip='10.0.0.4/8', position='49,48,0', range=50)
    sta5 = net.addStation('sta5', mac='00:00:00:00:00:06', ip='10.0.0.5/8', position='50,48,0', range=50)
    sta6 = net.addStation('sta6', mac='00:00:00:00:00:07', ip='10.0.0.6/8', position='51,48,0', range=50)
    
    sta7 = net.addStation('sta7', mac='00:00:00:00:00:08', ip='10.0.0.7/8', position='54,52,0', range=50)
    sta8 = net.addStation('sta8', mac='00:00:00:00:00:09', ip='10.0.0.8/8', position='55,52,0', range=50)
    sta9 = net.addStation('sta9', mac='00:00:00:00:00:10', ip='10.0.0.9/8', position='56,52,0', range=50)

    ap1 = net.addAccessPoint('ap1', ssid='new-ssid1', mode='g', channel='1', position='45,50,0', range=25)
    ap2 = net.addAccessPoint('ap2', ssid='new-ssid2', mode='g', channel='6', position='50,50,0', range=25)
    ap3 = net.addAccessPoint('ap3', ssid='new-ssid3', mode='g', channel='11', position='55,50,0', range=25)

    c1 = net.addController('c1', controller=Controller)

    h1 = net.addHost('h1', ip='10.0.2.10/8', mac='00:00:00:00:10:00')
    h2 = net.addHost('h2', ip='10.0.2.11/8', mac='00:00:00:00:11:00')
    h3 = net.addHost('h3', ip='10.0.2.12/8', mac='00:00:00:00:12:00')

    sw1 = net.addSwitch ('sw1', dpid='9', protocols='OpenFlow13')
    sw2 = net.addSwitch ('sw2', dpid='10', protocols='OpenFlow13')
    sw3 = net.addSwitch ('sw3', dpid='11', protocols='OpenFlow13')
    sw4 = net.addSwitch ('sw4', dpid='12', protocols='OpenFlow13')
    sw5 = net.addSwitch ('sw5', dpid='13', protocols='OpenFlow13')

    net.propagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")

    net.addLink(h1, sw2, 0, 1)
    net.addLink(h2, sw2, 0, 2)
    net.addLink(h3, sw2, 0, 3)
    net.addLink(sw3, ap1, 1, 3)
    net.addLink(sw4, ap2, 2, 4)
    net.addLink(sw5, ap3, 3, 3)
    link1 = net.addLink(sw1, sw2, 1, 4, cls=TCLink )
    link2 = net.addLink(sw3, sw1, 3, 2, cls=TCLink)
    link3 = net.addLink(sw4, sw1, 4, 3, cls=TCLink)
    link4 = net.addLink(sw5, sw1, 5, 4, cls=TCLink)

    print( "*** Configuring links bandwidth" )
    link1.intf1.config( bw=17 )
    link2.intf1.config( bw=1, delay='20ms', loss=1) #Wifi (AP1)
    link3.intf1.config( bw=1, delay='120ms', loss=5) #LTE (AP2)
    link4.intf1.config( bw=1, delay='500ms', loss=10) #D2D (AP3)

    net.plotGraph(max_x=100, max_y=100)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    sw1.start([c1])
    sw2.start([c1])
    sw3.start([c1])
    sw4.start([c1])
    sw5.start([c1])

    time.sleep(5)
    os.system('ovs-ofctl del-flows sw1 -O Openflow13; ovs-ofctl add-flow sw1 "table=0, priority=0, actions=goto_table:1" -O Openflow13;')
    os.system('ovs-ofctl del-flows sw2 -O Openflow13; ovs-ofctl add-flow sw2 "table=0, priority=0, actions=goto_table:1" -O Openflow13;')
    os.system('ovs-ofctl del-flows sw3 -O Openflow13; ovs-ofctl add-flow sw3 "table=0, priority=0, actions=goto_table:1" -O Openflow13;\
        ovs-ofctl add-flow sw3 "table=1, priority=0, in_port=3 actions=1" -O Openflow13; ovs-ofctl add-flow sw3 "table=1, priority=0,\
        in_port=1 actions=3" -O Openflow13;')
    os.system('ovs-ofctl del-flows sw4 -O Openflow13; ovs-ofctl add-flow sw4 "table=0, priority=0, actions=goto_table:1" -O Openflow13;\
        ovs-ofctl add-flow sw4 "table=1, priority=0, in_port=2 actions=4" -O Openflow13; ovs-ofctl add-flow sw4 "table=1, priority=0,\
        in_port=4 actions=2" -O Openflow13;')
    os.system('ovs-ofctl del-flows sw5 -O Openflow13; ovs-ofctl add-flow sw5 "table=0, priority=0, actions=goto_table:1" -O Openflow13;\
        ovs-ofctl add-flow sw5 "table=1, priority=0, in_port=3 actions=5" -O Openflow13; ovs-ofctl add-flow sw5 "table=1, priority=0,\
        in_port=5 actions=3" -O Openflow13;')
    os.system('ovs-ofctl del-flows ap1 -O Openflow13; ovs-ofctl add-flow ap1 "table=0, priority=0, actions=goto_table:1" -O Openflow13;\
        ovs-ofctl add-flow ap1 "table=1, priority=0, in_port=1, actions=3" -O Openflow13; ovs-ofctl add-flow ap1 "table=1, priority=0, \
        in_port=3, actions=1" -O Openflow13;')
    os.system('ovs-ofctl del-flows ap2 -O Openflow13; ovs-ofctl add-flow ap2 "table=0, priority=0, actions=goto_table:1" -O Openflow13;\
        ovs-ofctl add-flow ap2 "table=1, priority=0, in_port=1, actions=4" -O Openflow13; ovs-ofctl add-flow ap2 "table=1, priority=0, \
        in_port=4, actions=1" -O Openflow13;')
    os.system('ovs-ofctl del-flows ap3 -O Openflow13; ovs-ofctl add-flow ap3 "table=0, priority=0, actions=goto_table:1" -O Openflow13; \
        ovs-ofctl add-flow ap3 "table=1, priority=0, in_port=1, actions=3" -O Openflow13; ovs-ofctl add-flow ap3 "table=1, priority=0, \
        in_port=3, actions=1" -O Openflow13;')

    #Necessary to avoid icmp noise
    h1.cmd('iptables -I OUTPUT -p icmp --icmp-type destination-unreachable -j DROP')
    h2.cmd('iptables -I OUTPUT -p icmp --icmp-type destination-unreachable -j DROP')
    h3.cmd('iptables -I OUTPUT -p icmp --icmp-type destination-unreachable -j DROP')
    time.sleep(1)

    #Removing trace files and stopping network manager
    os.system('rm -f sta*; rm -f h?*; rm -f ping*; rm -f delay*; rm log*; /etc/init.d/network-manager stop')
    time.sleep(2)

    info("*** alimentando MACs\n")

    h1.cmd('arp -f ./mac2iot.txt &')
    time.sleep(0.5)
    h2.cmd('arp -f ./mac2iot.txt &')
    time.sleep(0.5)
    h3.cmd('arp -f ./mac2iot.txt &')
    time.sleep(0.5)
    
    sta1.cmd('arp -f ./mac2iot.txt &')
    time.sleep(0.5)
    sta2.cmd('arp -f ./mac2iot.txt &')
    time.sleep(0.5)
    sta3.cmd('arp -f ./mac2iot.txt &')
    time.sleep(0.5)

    sta4.cmd('arp -f ./mac2iot.txt &')
    time.sleep(0.5)

    sta5.cmd('arp -f ./mac2iot.txt &')
    time.sleep(0.5)

    sta6.cmd('arp -f ./mac2iot.txt &')
    time.sleep(0.5)

    sta7.cmd('arp -f ./mac2iot.txt &')
    time.sleep(0.5)

    sta8.cmd('arp -f ./mac2iot.txt &')
    time.sleep(0.5)

    sta9.cmd('arp -f ./mac2iot.txt &')
    time.sleep(0.5)

    if flag == '-pv':
        print( "*** Using papers version")

        # SH (H1) - sta1, sta4, sta7 - via LTE (AP2)
        # GI (H2) - sta2, sta5, sta8 - via D2D (AP3)
        # IM (H3) - sta3, sta6, sta9 - via wifi (AP1)

        info("*** Configurando conexoes e tabelas no SW1\n")
        sta1.cmd('iw dev sta1-wlan0 disconnect')
        time.sleep(1)
        sta1.cmd('iw dev sta1-wlan0 connect new-ssid2')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=3,dl_src=00:00:00:00:00:02 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:02 actions=3" -O Openflow13')
        
        sta2.cmd('iw dev sta2-wlan0 disconnect')
        time.sleep(1)
        sta2.cmd('iw dev sta2-wlan0 connect new-ssid3')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=4,dl_src=00:00:00:00:00:03 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:03 actions=4" -O Openflow13')
        
        sta3.cmd('iw dev sta3-wlan0 disconnect')
        time.sleep(1)
        sta3.cmd('iw dev sta3-wlan0 connect new-ssid1')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=2,dl_src=00:00:00:00:00:04 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:04 actions=2" -O Openflow13')

        sta4.cmd('iw dev sta4-wlan0 disconnect')
        time.sleep(1)
        sta4.cmd('iw dev sta4-wlan0 connect new-ssid2')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=3,dl_src=00:00:00:00:00:05 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:05 actions=3" -O Openflow13')
        
        sta5.cmd('iw dev sta5-wlan0 disconnect')
        time.sleep(1)
        sta5.cmd('iw dev sta5-wlan0 connect new-ssid3')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=4,dl_src=00:00:00:00:00:06 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:06 actions=4" -O Openflow13')
        
        sta6.cmd('iw dev sta6-wlan0 disconnect')
        time.sleep(1)
        sta6.cmd('iw dev sta6-wlan0 connect new-ssid1')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=2,dl_src=00:00:00:00:00:07 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:07 actions=2" -O Openflow13')

        sta7.cmd('iw dev sta7-wlan0 disconnect')
        time.sleep(1)
        sta7.cmd('iw dev sta7-wlan0 connect new-ssid2')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=3,dl_src=00:00:00:00:00:08 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:08 actions=3" -O Openflow13')
        
        sta8.cmd('iw dev sta8-wlan0 disconnect')
        time.sleep(1)
        sta8.cmd('iw dev sta8-wlan0 connect new-ssid3')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=4,dl_src=00:00:00:00:00:09 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:09 actions=4" -O Openflow13')
        
        sta9.cmd('iw dev sta9-wlan0 disconnect')
        time.sleep(1)
        sta9.cmd('iw dev sta9-wlan0 connect new-ssid1')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=2,dl_src=00:00:00:00:00:10 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:10 actions=2" -O Openflow13')        
        
    else:
        print( "*** Using default version")
        info("*** Configurando conexoes e tabelas no SW1\n")
        sta1.cmd('iw dev sta1-wlan0 disconnect')
        time.sleep(1)
        sta1.cmd('iw dev sta1-wlan0 connect new-ssid1')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=2,dl_src=00:00:00:00:00:02 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:02 actions=2" -O Openflow13')

        sta2.cmd('iw dev sta2-wlan0 disconnect')
        time.sleep(1)
        sta2.cmd('iw dev sta2-wlan0 connect new-ssid1')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=2,dl_src=00:00:00:00:00:03 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:03 actions=2" -O Openflow13')

        sta3.cmd('iw dev sta3-wlan0 disconnect')
        time.sleep(1)
        sta3.cmd('iw dev sta3-wlan0 connect new-ssid1')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=2,dl_src=00:00:00:00:00:04 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:04 actions=2" -O Openflow13')

        sta4.cmd('iw dev sta4-wlan0 disconnect')
        time.sleep(1)
        sta4.cmd('iw dev sta4-wlan0 connect new-ssid2')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=3,dl_src=00:00:00:00:00:05 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:05 actions=3" -O Openflow13')
        
        sta5.cmd('iw dev sta5-wlan0 disconnect')
        time.sleep(1)
        sta5.cmd('iw dev sta5-wlan0 connect new-ssid2')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=3,dl_src=00:00:00:00:00:06 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:06 actions=3" -O Openflow13')

        sta6.cmd('iw dev sta6-wlan0 disconnect')
        time.sleep(1)
        sta6.cmd('iw dev sta6-wlan0 connect new-ssid2')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=3,dl_src=00:00:00:00:00:07 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:07 actions=3" -O Openflow13')
        
        sta7.cmd('iw dev sta7-wlan0 disconnect')
        time.sleep(1)
        sta7.cmd('iw dev sta7-wlan0 connect new-ssid3')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=4,dl_src=00:00:00:00:00:08 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:08 actions=4" -O Openflow13')
        
        sta8.cmd('iw dev sta8-wlan0 disconnect')
        time.sleep(1)
        sta8.cmd('iw dev sta8-wlan0 connect new-ssid3')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=4,dl_src=00:00:00:00:00:09 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:09 actions=4" -O Openflow13')

        sta9.cmd('iw dev sta9-wlan0 disconnect')
        time.sleep(1)
        sta9.cmd('iw dev sta9-wlan0 connect new-ssid3')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=4,dl_src=00:00:00:00:00:10 actions=1" -O Openflow13')
        os.system('ovs-ofctl add-flow sw1 "table=1, priority=1, cookie=0x0, in_port=1,dl_dst=00:00:00:00:00:10 actions=4" -O Openflow13')      
    

    info("*** Configurando tabelas SW2\n")
    
    
    os.system('ovs-ofctl add-flow sw2 "table=1, priority=1, cookie=0x0, in_port=1,dl_src=00:00:00:00:10:00 actions=4" -O Openflow13')
    os.system('ovs-ofctl add-flow sw2 "table=1, priority=1, cookie=0x0, in_port=4,nw_dst=10.0.2.10,icmp actions=1" -O Openflow13')
    os.system('ovs-ofctl add-flow sw2 "table=1, priority=1, cookie=0x0, in_port=4,nw_dst=10.0.2.10,udp actions=1" -O Openflow13')

    os.system('ovs-ofctl add-flow sw2 "table=1, priority=1, cookie=0x0, in_port=2,dl_src=00:00:00:00:11:00 actions=4" -O Openflow13')
    os.system('ovs-ofctl add-flow sw2 "table=1, priority=1, cookie=0x0, in_port=4,nw_dst=10.0.2.11,icmp actions=2" -O Openflow13')
    os.system('ovs-ofctl add-flow sw2 "table=1, priority=1, cookie=0x0, in_port=4,nw_dst=10.0.2.11,udp actions=2" -O Openflow13')

    os.system('ovs-ofctl add-flow sw2 "table=1, priority=1, cookie=0x0, in_port=3,dl_src=00:00:00:00:12:00 actions=4" -O Openflow13')
    os.system('ovs-ofctl add-flow sw2 "table=1, priority=1, cookie=0x0, in_port=4,nw_dst=10.0.2.12,icmp actions=3" -O Openflow13')
    os.system('ovs-ofctl add-flow sw2 "table=1, priority=1, cookie=0x0, in_port=4,nw_dst=10.0.2.12,udp actions=3" -O Openflow13')

    info("*** Starting tcpdump in servers\n")

    h1.cmd('tcpdump udp port 5001 -i h1-eth0 --direction=in -tttttnnvS --immediate-mode -l > h1.txt &')
    h2.cmd('tcpdump udp port 5002 -i h2-eth0 --direction=in -tttttnnvS --immediate-mode -l > h2.txt &')
    h3.cmd('tcpdump udp port 5003 -i h3-eth0 --direction=in -tttttnnvS --immediate-mode -l > h3.txt &')


    time.sleep(5)

    info("*** Starting stations clients\n")

    sta1.cmd('./iotsdn/carconiotsh.sh &')
    sta2.cmd('./iotsdn/carconiotgi.sh &')
    sta3.cmd('./iotsdn/carconiotim.sh &')
    sta4.cmd('./iotsdn/carconiotsh.sh &')
    sta5.cmd('./iotsdn/carconiotgi.sh &')
    sta6.cmd('./iotsdn/carconiotim.sh &')
    sta7.cmd('./iotsdn/carconiotsh.sh &')
    sta8.cmd('./iotsdn/carconiotgi.sh &')
    sta9.cmd('./iotsdn/carconiotim.sh &')

    info("*** Waiting to finish\n")

    time.sleep(305)

    #Finishing process
    os.system('pkill tcpdump')
    os.system('pkill hping3')
    os.system('pkill ping')
    time.sleep(2)

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    flag = sys.argv[1]
    if flag == '-pv':
        print( "*** Using papers version...")
    else:
        print( "*** Using default version")
    topology(flag)
