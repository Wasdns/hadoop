#!/usr/bin/env python
import sys
import struct
import argparse
import commands

from scapy.all import sniff, sendp, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import IP, TCP, ICMP, UDP, Raw 

parser = argparse.ArgumentParser(description='Receiver')
parser.add_argument('-p', '--port', help='listen port', 
                    type=str, action="store", default='ens2f0')
args = parser.parse_args()

counter = 0

def handle_pkt(packet):
    global counter
    counter = counter+1
    return 'Packet #{}: {} ==> {}'.format(counter, packet[0][1].src, packet[0][1].dst)

def main():
    # Get Thrift Port
    iface = args.port
    print "sniffing on %s" % iface
    sys.stdout.flush()
    sniff(filter="ip", iface = iface, prn = lambda x: handle_pkt(x))

if __name__ == '__main__':
    main()

