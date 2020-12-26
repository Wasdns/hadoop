#!/usr/bin/env python

import argparse
import sys
import socket
import random
import struct

from scapy.all import *
from time import sleep

parser = argparse.ArgumentParser(description='Generating flows')
parser.add_argument('--dl-src', help='Data Link source address',
                    type=str, action="store", default='00:00:00:00:00:01')
parser.add_argument('--dl-dst', help='Data Link destination address',
                    type=str, action="store", default='9c:69:b4:60:35:24')
parser.add_argument('--nw-src', help='Network source address',
                    type=str, action="store", default='10.0.0.25')
parser.add_argument('--nw-dst', help='Network destination address',
                    type=str, action="store", default='10.0.0.26')
parser.add_argument('--nw-proto', help='Network Layer protocol',
                    type=int, action="store", default=6)
parser.add_argument('--srcPort', help='L4 Source port',
                    type=int, action="store", default=520)
parser.add_argument('--dstPort', help='L4 Destination port',
                    type=int, action="store", default=10)
parser.add_argument('-n', '--num', help='total number',
                    type=int, action="store", default=100)
parser.add_argument('-r', '--rate', help='packet sending rate (packets per second, pps)',
                    type=int, action="store", default=100)
parser.add_argument('-i', '--iface', help='Interface',
                    type=str, action="store", default='ens2f0')
parser.add_argument('-t', '--interval', help='Time interval between two packets',
                    type=float, action="store", default=0)
parser.add_argument('--random', help='Random packets',
                    type=int, action="store", default=1)
args = parser.parse_args()

def TCPPacket(dl_src, dl_dst, nw_src, nw_dst, nw_proto, srcPort, dstPort, random=0):
    if random == 1:
    	return Ether(src=dl_src, dst=dl_dst) / IP(src=RandIP(), dst=nw_dst) / TCP(sport=srcPort, dport=dstPort)
    else:
        return Ether(src=dl_src, dst=dl_dst) / IP(src=nw_src, dst=nw_dst) / TCP(sport=srcPort, dport=dstPort)

def UDPPacket(dl_src, dl_dst, nw_src, nw_dst, nw_proto, srcPort, dstPort, random=0):
    if random == 1:
        return Ether(src=dl_src, dst=dl_dst, type=0x800) / IP(src=RandIP(), dst=nw_dst, proto=17) / UDP(sport=srcPort,dport=dstPort) / "6x1"
    else:
        return Ether(src=dl_src, dst=dl_dst, type=0x800) / IP(src=nw_src, dst=nw_dst, proto=17) / UDP(sport=srcPort,dport=dstPort) / "6x1"

def main():
    dl_src, dl_dst = args.dl_src, args.dl_dst
    nw_src, nw_dst = args.nw_src, args.nw_dst
    nw_proto = args.nw_proto
    srcPort, dstPort = args.srcPort, args.dstPort
    num, iface = args.num, args.iface
    t = args.interval
    rate = args.rate

    pkt_list = []

    for i in range(num):
        if nw_proto == 6:
            pkt = TCPPacket(dl_src, dl_dst, nw_src, nw_dst, nw_proto, srcPort, dstPort, args.random)
        elif nw_proto == 17:
            pkt = UDPPacket(dl_src, dl_dst, nw_src, nw_dst, nw_proto, srcPort, dstPort, args.random)
        pkt_list.append(pkt)
        sendp(pkt, iface=iface)
        sleep(t)

    #sendpfast(pkt_list, pps=rate, iface=iface)

if __name__ == '__main__':
    main()
