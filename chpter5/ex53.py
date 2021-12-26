import sys
i, o, e = sys.stdin, sys.stdout, sys.stderr
from scapy.all import *
sys.stdin, sys.stdout, sys.stderr = i, o, e

from scapy.layers.dns import DNS, DNSQR, DNSRR

from scapy.layers.inet import IP, TCP, UDP


def print_query_name(dns_packet):
    print(dns_packet[DNSQR].qname)


def filter_dns(packet):
    return (DNS in packet and packet[DNS].opcode == 0 and packet[DNSQR].qtype == 1)

my_packet = IP(dst = "www.google.com") / Raw("Hello")
