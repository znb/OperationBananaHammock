#!/usr/bin/python
# send a dhcp discover packet

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

conf.verb = 0
conf.checkIPaddr = False

print "Building packet"
e = Ether(dst="ff:ff:ff:ff:ff:ff")
i = IP(src="0.0.0.0",dst="255.255.255.255")
u = UDP(sport=68,dport=67)
# You will just need to modify the chaddr address below
b = BOOTP(chaddr="00:0c:29:be:e4:6d",xid=31337)
d = DHCP(options=[("message-type","discover"),"end"])

dhcp_discover = e/i/u/b/d

print "Sending packet"
reply = srp(dhcp_discover, iface="eth0", timeout=3)
for a in reply:
	print a.show()
