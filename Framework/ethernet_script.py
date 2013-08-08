#!/usr/bin/python
# Framework that pulls everything together

import sys
import argparse
from scapy.all import *


def packet_gen(args):

    print "Firing up the ION laser"
    print "Our gateway is: " + args.gateway

    print "Putting packet together: ",
    # Assemble the various packet bits here
    print "Ethernet,",
    print "ARP,",
    print "DHCP,",
    print "DNS,",
    print "HTTP",

    print "\nSending packet"
    # Send the entire packet here

    print "Response"
    # Get/Print the response here

    print "We're done here"


def __main__():

    parser = argparse.ArgumentParser(description='Scapy for the win', usage='%(prog)s -g gateway')
    parser.add_argument('--gateway', '-g', dest='gateway', help='network gateway')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()

    if not args.gateway:
        sys.exit(parser.print_help())

    packet_gen(args)


if __name__ == '__main__':
    __main__()


