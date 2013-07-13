#!/usr/bin/python
# Simple DNS request

from scapy.all import *
import sys

# EDIT ME
RESOLVER="8.8.8.8"
HOST="blog.zonbi.org"

a = sr1(IP(dst=RESOLVER)/UDP()/DNS(rd=1,qd=DNSQR(qname=HOST)),verbose=0)
print "Host: " + HOST + " >> " + a[DNSRR].rdata
    

