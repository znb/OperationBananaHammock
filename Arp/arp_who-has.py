#!/usr/bin/python
# send arp "who-has" request

from scapy.all import *
import sys

print "building packet: ",
print "Ethernet/",
e = Ether()
e.type=int("0x806", 16)
print "Arp",
a = ARP()
a.hwtype=int("0x1", 16)
a.hwlen=int("6")
a.plen=int("4")
a.op="who-has"
a.pdst="172.16.0.1"
a.hwsrc="00:0c:29:be:e4:77"
a.psrc="172.16.0.200"
a.hwdst="ff:ff:ff:ff:ff:ff" 
packet = e/a
print "\n"

print "sending packet on layer 2"
sendp(packet, iface="eth0")
