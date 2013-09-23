#!/usr/bin/python
# send arp "who-has" request


import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


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
a.psrc="10.0.0.71"
a.pdst="10.0.0.253"
packet = e/a

print "\nSending packet on layer 2"
ans,unans = srp(packet, iface="eth0")
for snd,rcv in ans:
    macaddy = rcv.sprintf(r"%Ether.src%")

print "MAC address for: " + a.pdst + " is " + macaddy

