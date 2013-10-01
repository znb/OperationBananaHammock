#!/usr/bin/python

# simple icmp traceroute script

import sys 
import argparse
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


def traceroute(atarget, amhops):

    print "begin trace... " + atarget
    ans,unans=sr(IP(dst=atarget,ttl=(1,int(amhops))/ICMP()))
    print "Traceroute: " + atarget
    ans.summary(lambda(s,r) : r.sprintf("%IP.src%"))


def menu():

    parser = argparse.ArgumentParser(description='simple traceroute in scapy', usage='%(prog)s -t target')
    parser.add_argument('--target', '-t', dest='target', help='target to trace')
    parser.add_argument('--max-hops', '-m', dest='mhops', help='maximum hops', default=30)
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()

    if not args.target:
        sys.exit(parser.print_help())

    atarget = args.target
    amhops = args.mhops
    traceroute(atarget, amhops)


if __name__ == '__main__':
    menu()
