#!/usr/bin/python
# Simple HTTP Request

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

HOSTNAME="www.brucon.org"
GETREQ="GET / HTTP/1.1\r\nHost: www.brucon.org\r\n\r\n"

print "Syn"
syn = IP(dst=HOSTNAME) / TCP(sport=666, dport=80, flags='S')
print "Syn/Ack"
syn_ack = sr1(syn)
print "TCP Sequencing"
request = IP(dst=HOSTNAME) / TCP(dport=80, sport=syn_ack[TCP].dport,seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / GETREQ
print "Reply"
reply = sr1(request)
reply.show()

print "We're done here"
