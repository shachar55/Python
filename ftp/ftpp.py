from scapy.all import *
from scapy.layers.inet import IP, ICMP
import sys


def the_filter(pack):
    return ICMP in pack


def main(dest, file):
    print("Server running...")
    last_packet = 0
    while True:
        pack = sniff(count=1, lfilter=the_filter)[0]
        pack_data = pack[Raw].load
        packet_num = int(pack_data[0])
        packet_flag = int(pack_data[1])
        if packet_flag == 1:
            break
        if packet_num == last_packet + 1:
            with open(file, "wb") as f:
                f.write(pack_data[3:])
            last_packet += 1

        to_send = IP(dst=dest) / ICMP(type="echo-reply") / Raw(bytes(last_packet))
        send(to_send)
        if packet_num == 255:
            last_packet = 0

    print("The image was saved successfully")


if __name__ == "__main__":
    #main(sys.argv[1], sys.argv[2])
    main('192.168.99.163',"/media/kali/SHACHAR'\''S/Python/ftp/data")