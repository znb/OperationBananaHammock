#!/usr/bin/python
# send arp "who-has" request

from scapy.all import *

print "building packet"
a = ARP()
a.hwtype="0x1"
a.ptype="0x800"
a.hwlen="6"
a.plen="4"
a.op="who-has"
a.pdst="172.16.0.1"
a.hwsrc="00:0c:29:be:e4:77"
a.psrc="172.16.0.10"
a.hwdst="ff:ff:ff:ff:ff:ff" 

print "sending packet on layer 2"
sendp(a, iface="eth1")
