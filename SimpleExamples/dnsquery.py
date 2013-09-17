#!/usr/bin/python
# Silly DNS resolver which will default to Google if you let it

import argparse
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


def lookup(adomain, aresolver):
    """lookup a domain"""    
    a = sr1(IP(dst=aresolver)/UDP()/DNS(rd=1,qd=DNSQR(qname=adomain)),verbose=0)    
    return a[DNSRR].rdata  
    

def menu():

    parser = argparse.ArgumentParser(description='basic DNS query', usage='%(prog)s -d domain -r resolver')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.2')
    parser.add_argument('--domain', '-d', dest='domain', help='domain to lookup')
    parser.add_argument('--resolver', '-r', dest='resolver', help='resolver to use', default='8.8.8.8')
    args = parser.parse_args()
    adomain = args.domain
    aresolver = args.resolver

    if not args.domain:
        sys.exit(parser.print_help())

    output = lookup(adomain, aresolver)
    print adomain + " >> " + output + "  (%s)" % aresolver


if __name__ == '__main__':
    menu()
