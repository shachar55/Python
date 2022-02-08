from scapy.all import *
from scapy.layers.inet import IP,ICMP
import dnspython as dns
import dns.resolver


def main():
    count = 1
    domain = "www.google.com"
    ip = py


    
    while True:
        tracert_packet = IP(ttl = count,dst = ip)/ICMP()
        tracert_response = sr1(tracert_packet)/ICMP()
        print("s")
        if tracert_response[IP].src == ip:
            break
    
    print(f"{count} hops")