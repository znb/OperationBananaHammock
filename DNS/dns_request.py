#!/usr/bin/python3
# Simple DNS request with enhanced functionality

import logging
import argparse
import sys
import time
from scapy.all import IP, UDP, DNS, DNSQR, DNSRR, sr1

# Suppress Scapy runtime warnings
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# DNS record type mapping
DNS_TYPES = {
    'A': 1,
    'AAAA': 28,
    'MX': 15,
    'CNAME': 5,
    'NS': 2,
    'TXT': 16,
    'PTR': 12,
    'SOA': 6
}


def validate_hostname(hostname):
    """Basic validation for hostname"""
    if not hostname or len(hostname) > 253:
        return False
    return True


def perform_dns_query(resolver, hostname, query_type='A', timeout=5, verbose=False):
    """
    Perform a DNS query using Scapy

    Args:
        resolver: DNS server IP address
        hostname: Hostname to resolve
        query_type: DNS query type (A, AAAA, MX, etc.)
        timeout: Query timeout in seconds
        verbose: Enable verbose output

    Returns:
        DNS response or None if failed
    """
    if not validate_hostname(hostname):
        print(f"Error: Invalid hostname '{hostname}'")
        return None

    # Get DNS query type code
    qtype = DNS_TYPES.get(query_type.upper(), 1)

    try:
        print(f"Querying {resolver} for {hostname} ({query_type} record)...")
        start_time = time.time()

        # Perform DNS query
        response = sr1(
            IP(dst=resolver)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=hostname, qtype=qtype)),
            verbose=0 if not verbose else 1,
            timeout=timeout
        )

        elapsed_time = time.time() - start_time

        if response is None:
            print(f"Error: No response received (timeout after {timeout}s)")
            return None

        if not response.haslayer(DNS):
            print("Error: Response does not contain DNS layer")
            return None

        # Check for DNS errors
        dns_layer = response[DNS]
        if dns_layer.rcode != 0:
            rcode_messages = {
                1: "Format error",
                2: "Server failure",
                3: "Name error (domain does not exist)",
                4: "Not implemented",
                5: "Refused"
            }
            error_msg = rcode_messages.get(dns_layer.rcode, f"Unknown error (rcode: {dns_layer.rcode})")
            print(f"DNS Error: {error_msg}")
            return None

        # Display results
        print(f"\n{'='*60}")
        print(f"DNS Query Results (response time: {elapsed_time*1000:.2f}ms)")
        print(f"{'='*60}")

        if dns_layer.ancount == 0:
            print("No answers found")
            return response

        # Process all answer records
        answer_count = 0
        current = dns_layer.an

        while current:
            if isinstance(current, DNSRR):
                answer_count += 1
                rdata = current.rdata

                # Format rdata based on type
                if isinstance(rdata, bytes):
                    try:
                        rdata = rdata.decode('utf-8')
                    except:
                        rdata = str(rdata)

                print(f"\nAnswer {answer_count}:")
                print(f"  Name:  {current.rrname.decode() if isinstance(current.rrname, bytes) else current.rrname}")
                print(f"  Type:  {current.type} ({current.sprintf('%DNS.type%')})")
                print(f"  Class: {current.sprintf('%DNS.rclass%')}")
                print(f"  TTL:   {current.ttl}s")
                print(f"  Data:  {rdata}")

            current = current.payload if hasattr(current, 'payload') and current.payload.name != 'NoPayload' else None

        print(f"\n{'='*60}\n")

        return response

    except KeyboardInterrupt:
        print("\nQuery interrupted by user")
        return None
    except Exception as e:
        print(f"Error performing DNS query: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return None


def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(
        description='Perform DNS queries using Scapy',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s www.brucon.org
  %(prog)s www.brucon.org -r 1.1.1.1
  %(prog)s google.com -t AAAA
  %(prog)s google.com -t MX -r 8.8.8.8 -v
        """
    )

    parser.add_argument('hostname', help='Hostname to resolve')
    parser.add_argument('-r', '--resolver', default='8.8.8.8',
                        help='DNS resolver IP address (default: 8.8.8.8)')
    parser.add_argument('-t', '--type', default='A', choices=list(DNS_TYPES.keys()),
                        help='DNS query type (default: A)')
    parser.add_argument('-T', '--timeout', type=float, default=5.0,
                        help='Query timeout in seconds (default: 5.0)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output')

    args = parser.parse_args()

    response = perform_dns_query(
        resolver=args.resolver,
        hostname=args.hostname,
        query_type=args.type,
        timeout=args.timeout,
        verbose=args.verbose
    )

    # Exit with appropriate status code
    sys.exit(0 if response else 1)


if __name__ == '__main__':
    main()
