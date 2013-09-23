#!/usr/bin/python
# send a dhcp request packet

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


print "Pre-game"
conf.verb = 0
conf.checkIPaddr = False
hw="00:0c:29:be:e4:6d"
print "Building packet"

e = Ether(dst="ff:ff:ff:ff:ff:ff")
i = IP(src="0.0.0.0",dst="255.255.255.255")
u = UDP(sport=68,dport=67)
b = BOOTP(chaddr=hw,xid=31337)
d = DHCP(options=[("message-type","request"),IPField("requested_addr","192.168.0.12"),"end"])

dhcp_request = e/i/u/b/d

print "Sending packet"
reply = srp(dhcp_request, iface="eth0", timeout=3)
for a in reply:
	print a.show()

print "We're done here"
