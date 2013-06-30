#!/usr/bin/python

# Silly DNS resolver

from scapy.all import *
import argparse
import sys

RESOLVER="8.8.8.8"


def lookup(arg_domain):
    """lookup a domain"""
    a = sr1(IP(dst=RESOLVER)/UDP()/DNS(rd=1,qd=DNSQR(qname=arg_domain)),verbose=0)
    return a[DNSRR].rdata
    

def menu():

    parser = argparse.ArgumentParser(description='basic DNS query', usage='%(prog)s -d domain')
    parser.add_argument('--domain', '-d', dest='domain', help='domain to lookup')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    arg_domain = args.domain

    if not args.domain:
        sys.exit(parser.print_help())

    output = lookup(arg_domain)
    print arg_domain + " >> " + output


if __name__ == '__main__':
    menu()

