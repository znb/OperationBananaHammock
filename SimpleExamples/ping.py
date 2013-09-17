#!/usr/bin/python

# simple ping script

import sys 
import argparse
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


def ping(atarget):

    conf.verb = 0
    tout = 2
    print "generation"
    tcp = IP(dst=atarget)
    ping = ICMP()
    packet = tcp/ping
    print "packeting... " + atarget 
    reply = sr1(packet, timeout=tout)
    if not (reply is None):
         print reply.src, "is online"
    else:
         print "Timeout waiting for " + atarget


def menu():

    parser = argparse.ArgumentParser(description='simple ping script', usage='%(prog)s -t target')
    parser.add_argument('--target', '-t', dest='target', help='target to trace')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()

    if not args.target:
        sys.exit(parser.print_help())

    atarget = args.target
    ping(atarget)


if __name__ == '__main__':
    menu()
