#!/usr/bin/python3
# Send ARP "who-has" request with enhanced functionality

import logging
import argparse
import sys
import netifaces
from scapy.all import Ether, ARP, srp, conf, get_if_hwaddr, get_if_list

# Suppress Scapy runtime warnings
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


def get_local_interfaces():
    """Get list of available network interfaces"""
    try:
        return get_if_list()
    except:
        return []


def get_interface_mac(interface):
    """Get MAC address for a given interface"""
    try:
        return get_if_hwaddr(interface)
    except:
        return None


def validate_ip(ip_address):
    """Basic IP address validation"""
    parts = ip_address.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


def validate_mac(mac_address):
    """Basic MAC address validation"""
    parts = mac_address.split(':')
    if len(parts) != 6:
        return False
    try:
        return all(0 <= int(part, 16) <= 255 for part in parts)
    except ValueError:
        return False


def perform_arp_request(target_ip, source_mac=None, interface="eth0", timeout=2, verbose=False):
    """
    Perform an ARP who-has request

    Args:
        target_ip: Target IP address to resolve
        source_mac: Source MAC address (auto-detected if None)
        interface: Network interface to use
        timeout: Request timeout in seconds
        verbose: Enable verbose output

    Returns:
        MAC address if found, None otherwise
    """
    if not validate_ip(target_ip):
        print(f"Error: Invalid IP address '{target_ip}'")
        return None

    # Auto-detect source MAC if not provided
    if source_mac is None:
        source_mac = get_interface_mac(interface)
        if source_mac is None:
            print(f"Error: Could not detect MAC address for interface '{interface}'")
            print("Please specify a source MAC address manually with -m/--mac")
            return None
        if verbose:
            print(f"Auto-detected MAC address: {source_mac}")
    else:
        if not validate_mac(source_mac):
            print(f"Error: Invalid MAC address '{source_mac}'")
            return None

    try:
        # Disable Scapy verbosity unless verbose mode
        original_verb = conf.verb
        conf.verb = 0 if not verbose else 1

        print(f"Building ARP packet for {target_ip}...")

        # Build Ethernet layer
        ether = Ether()
        ether.dst = "ff:ff:ff:ff:ff:ff"  # Broadcast
        ether.type = 0x806  # ARP

        # Build ARP layer
        arp = ARP()
        arp.op = "who-has"
        arp.hwsrc = source_mac
        arp.pdst = target_ip

        # Combine layers
        packet = ether/arp

        if verbose:
            print("\nPacket details:")
            packet.show()

        print(f"\nSending ARP request on {interface}...")

        # Send packet and wait for response
        answered, unanswered = srp(packet, iface=interface, timeout=timeout, verbose=0)

        # Restore original verbosity
        conf.verb = original_verb

        if not answered:
            print(f"No response received for {target_ip} (timeout after {timeout}s)")
            return None

        # Process responses
        print(f"\n{'='*60}")
        print(f"ARP Response")
        print(f"{'='*60}\n")

        mac_addresses = []
        for sent, received in answered:
            mac_addr = received.sprintf(r"%Ether.src%")
            mac_addresses.append(mac_addr)

            print(f"IP Address:  {target_ip}")
            print(f"MAC Address: {mac_addr}")

            if verbose:
                print(f"\nFull response:")
                received.show()

        print(f"\n{'='*60}\n")

        return mac_addresses[0] if mac_addresses else None

    except PermissionError:
        print("Error: Permission denied. This script requires root/administrator privileges.")
        print("Try running with sudo on Linux/Mac or as Administrator on Windows.")
        return None
    except OSError as e:
        if "No such device" in str(e):
            print(f"Error: Network interface '{interface}' not found")
            available = get_local_interfaces()
            if available:
                print(f"Available interfaces: {', '.join(available)}")
        else:
            print(f"Error: {e}")
        return None
    except KeyboardInterrupt:
        print("\nARP request interrupted by user")
        return None
    except Exception as e:
        print(f"Error performing ARP request: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return None


def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(
        description='Perform ARP who-has requests using Scapy',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sudo %(prog)s 192.168.1.1
  sudo %(prog)s 192.168.1.1 -i wlan0
  sudo %(prog)s 172.16.206.2 -m 00:0c:29:be:e4:6d -i eth0
  sudo %(prog)s 10.0.0.1 -t 5 -v

Note: This script requires root/administrator privileges to send raw packets.
        """
    )

    parser.add_argument('target_ip', help='Target IP address to resolve')
    parser.add_argument('-i', '--interface', default='eth0',
                        help='Network interface to use (default: eth0)')
    parser.add_argument('-m', '--mac',
                        help='Source MAC address (auto-detected if not specified)')
    parser.add_argument('-t', '--timeout', type=float, default=2.0,
                        help='Request timeout in seconds (default: 2.0)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output')
    parser.add_argument('-l', '--list-interfaces', action='store_true',
                        help='List available network interfaces and exit')

    args = parser.parse_args()

    # Handle list interfaces
    if args.list_interfaces:
        interfaces = get_local_interfaces()
        if interfaces:
            print("Available network interfaces:")
            for iface in interfaces:
                mac = get_interface_mac(iface)
                mac_info = f" (MAC: {mac})" if mac else ""
                print(f"  - {iface}{mac_info}")
        else:
            print("No network interfaces found")
        sys.exit(0)

    mac_address = perform_arp_request(
        target_ip=args.target_ip,
        source_mac=args.mac,
        interface=args.interface,
        timeout=args.timeout,
        verbose=args.verbose
    )

    # Exit with appropriate status code
    sys.exit(0 if mac_address else 1)


if __name__ == '__main__':
    main()
