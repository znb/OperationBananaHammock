#!/usr/bin/python
# send arp "who-has" request

from scapy.all import *
import sys

conf.verb = 0
print "Building packet",
e = Ether()
e.type=int("0x806", 16)
a = ARP()
a.hwtype=int("0x1", 16)
a.hwlen=int("6")
a.plen=int("4")
a.op="who-has"
a.hwsrc="00:0c:29:be:e4:6d"
a.hwdst="00:00:00:00:00:00" 
a.psrc="172.16.206.138"
a.pdst="172.16.206.2"
packet = e/a

print "\nSending packet on layer 2"
ans,unans = srp(packet, iface="eth0")
for snd,rcv in ans:
    macaddy = rcv.sprintf(r"%Ether.src%")

print "We wanted the MAC address for: " + a.pdst
print "We got: " + macaddy

