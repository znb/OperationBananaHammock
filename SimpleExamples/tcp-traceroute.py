#!/usr/bin/python

# simple traceroute script
# ps. I totally stole this from bsb

import sys 
import argparse
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


def traceroute(atarget):

    print "begin trace... " + atarget
    ans,unans=sr(IP(dst=atarget, ttl=(4,25),id=RandShort())/TCP(flags=0x2))
    print ""
    for snd,rcv in ans:
        print snd.ttl, rcv.src, isinstance(rcv.payload, TCP)        


def menu():

    parser = argparse.ArgumentParser(description='simple traceroute in scapy', usage='%(prog)s -t target')
    parser.add_argument('--target', '-t', dest='target', help='target to trace')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()

    if not args.target:
        sys.exit(parser.print_help())

    atarget = args.target
    traceroute(atarget)


if __name__ == '__main__':
    menu()
