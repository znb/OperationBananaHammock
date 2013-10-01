#!/usr/bin/python
# send arp "who-has" request


import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


conf.verb = 0
print "Building packet",
e = Ether()
e.dst="ff:ff:ff:ff:ff:ff"
e.type=0x806
a = ARP()
a.op="who-has"
a.hwsrc="00:0c:29:be:e4:6d"
a.pdst="172.16.206.2"
packet = e/a

print "\nSending packet on layer 2"
ans,unans = srp(packet, iface="eth0")
for snd,rcv in ans:
    macaddy = rcv.sprintf(r"%Ether.src%")

print "MAC address for: " + a.pdst + " is " + macaddy

