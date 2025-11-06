#!/usr/bin/env python3
"""
Network Scanner
A simple network scanner to discover active hosts and open ports on a network.
"""

import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple
import argparse


def scan_port(host: str, port: int, timeout: float = 1.0) -> Tuple[str, int, bool]:
    """
    Scan a single port on a host.
    
    Args:
        host: IP address or hostname to scan
        port: Port number to check
        timeout: Socket timeout in seconds
    
    Returns:
        Tuple of (host, port, is_open)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return (host, port, result == 0)
    except socket.error:
        return (host, port, False)


def scan_host(host: str, ports: List[int], timeout: float = 1.0) -> dict:
    """
    Scan multiple ports on a single host.
    
    Args:
        host: IP address or hostname to scan
        ports: List of ports to check
        timeout: Socket timeout in seconds
    
    Returns:
        Dictionary with host info and open ports
    """
    open_ports = []
    
    for port in ports:
        _, _, is_open = scan_port(host, port, timeout)
        if is_open:
            open_ports.append(port)
    
    return {
        'host': host,
        'open_ports': open_ports,
        'is_alive': len(open_ports) > 0
    }


def scan_network(network: str, ports: List[int], timeout: float = 1.0, max_workers: int = 50) -> List[dict]:
    """
    Scan all hosts in a network range.
    
    Args:
        network: Network in CIDR notation (e.g., '192.168.1.0/24')
        ports: List of ports to check
        timeout: Socket timeout in seconds
        max_workers: Maximum number of concurrent threads
    
    Returns:
        List of dictionaries with scan results for each host
    """
    results = []
    network_obj = ipaddress.ip_network(network, strict=False)
    
    print(f"[*] Scanning network: {network}")
    print(f"[*] Ports to scan: {ports}")
    print(f"[*] Total hosts: {network_obj.num_addresses}")
    print("-" * 50)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_host = {
            executor.submit(scan_host, str(host), ports, timeout): str(host)
            for host in network_obj.hosts()
        }
        
        for future in as_completed(future_to_host):
            result = future.result()
            if result['is_alive']:
                results.append(result)
                print(f"[+] Active host found: {result['host']}")
                print(f"    Open ports: {result['open_ports']}")
    
    return results


def main():
    """Main function to run the network scanner."""
    parser = argparse.ArgumentParser(
        description='Network Scanner - Discover active hosts and open ports'
    )
    parser.add_argument(
        'network',
        help='Network to scan in CIDR notation (e.g., 192.168.1.0/24)'
    )
    parser.add_argument(
        '-p', '--ports',
        help='Comma-separated list of ports to scan (default: common ports)',
        default='21,22,23,25,80,443,445,3306,3389,8080,8443'
    )
    parser.add_argument(
        '-t', '--timeout',
        type=float,
        help='Timeout for each connection attempt in seconds (default: 1.0)',
        default=1.0
    )
    parser.add_argument(
        '-w', '--workers',
        type=int,
        help='Maximum number of concurrent threads (default: 50)',
        default=50
    )
    
    args = parser.parse_args()
    
    # Parse ports
    try:
        ports = [int(p.strip()) for p in args.ports.split(',')]
    except ValueError:
        print("[!] Error: Invalid port format. Use comma-separated integers.")
        return
    
    # Validate network
    try:
        ipaddress.ip_network(args.network, strict=False)
    except ValueError:
        print("[!] Error: Invalid network format. Use CIDR notation (e.g., 192.168.1.0/24)")
        return
    
    # Run scan
    results = scan_network(args.network, ports, args.timeout, args.workers)
    
    # Summary
    print("\n" + "=" * 50)
    print(f"[*] Scan complete!")
    print(f"[*] Active hosts found: {len(results)}")
    
    if results:
        print("\n[*] Summary:")
        for result in results:
            print(f"    {result['host']}: {len(result['open_ports'])} open port(s)")


if __name__ == '__main__':
    main()
