parser start {
    return parse_ethernet;
}

header ethernet_t ethernet;

parser parse_ethernet {
    extract(ethernet);
    return select(latest.etherType) {
        0xfff : parse_diagnosis_header;
        default : parse_ipv4;
    }
}

header diagnosis_header_t diagnosis_hdr;

parser parse_diagnosis_header {
    extract(diagnosis_hdr);
    return ingress;//parse_ipv4;
}

#define IP_PROTOCOLS_TCP 6
#define IP_PROTOCOLS_UDP 17

header ipv4_t ipv4;

parser parse_ipv4 {
    extract(ipv4);
    return select(latest.protocol) {
        IP_PROTOCOLS_TCP : parse_tcp;
        IP_PROTOCOLS_UDP : parse_udp;
        default: ingress;
    }
}

metadata l4_t l4;

header tcp_t tcp;

parser parse_tcp {
    extract(tcp);
    set_metadata(l4.srcPort, tcp.srcPort);
    set_metadata(l4.dstPort, tcp.dstPort);
    return ingress;
}

header udp_t udp;

parser parse_udp {
    extract(udp);
    set_metadata(l4.srcPort, udp.srcPort);
    set_metadata(l4.dstPort, udp.dstPort);
    return ingress;
}
