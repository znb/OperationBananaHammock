#!/usr/bin/python
# send arp "who-has" request

from scapy.all import *

print "building packet"
a = ARP()
a.hwtype=int("0x1", 16)
a.ptype=int("0x800", 16)
a.hwlen=int("6")
a.plen=int("4")
a.op="who-has"
a.pdst="172.16.0.1"
a.hwsrc="00:0c:29:be:e4:77"
a.psrc="172.16.0.10"
a.hwdst="ff:ff:ff:ff:ff:ff" 

print "sending packet on layer 2"
sendp(a, iface="eth1")
