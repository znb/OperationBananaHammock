#!/usr/bin/python
# Simple DNS request

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


# EDIT ME
RESOLVER="8.8.8.8"
HOST="www.brucon.org"

a = sr1(IP(dst=RESOLVER)/UDP()/DNS(rd=1,qd=DNSQR(qname=HOST)),verbose=0)
print "Host: " + HOST + " >> " + a[DNSRR].rdata
    

