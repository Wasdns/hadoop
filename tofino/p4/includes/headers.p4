header_type ethernet_t {
    fields {
        dstAddr : 48;
        srcAddr : 48;
        etherType : 16;
    }
}

header_type diagnosis_header_t {
    fields {
        srcIP  : 32;
        dstIP  : 32;
	proto  : 8;
	srcPort : 16;
	dstPort : 16;
    }
}

header_type ipv4_t {
    fields {
        protocol_version : 4;
        ihl : 4;
        diffserv : 8;
        totalLen : 16;
        identification : 16;
        flags : 3;
        fragOffset : 13;
        ttl : 8;
        protocol : 8;
        hdrChecksum : 16;
        srcAddr : 32;
        dstAddr: 32;
    }
}

header_type tcp_t {
    fields {
        srcPort : 16;
        dstPort : 16;
        seqNo : 32;
        ackNo : 32;
        dataOffset : 4;
        res : 4;
        //cwr : 1;
        //ece : 1;
        //urg : 1;
        //ack : 1;
        //psh : 1;
        //rst : 1;
        //syn : 1;
        ctrl : 7;
        fin : 1;
        window : 16;
        checksum : 16;
        urgentPtr : 16;
    }
}

header_type udp_t {
    fields {
        srcPort : 16;
        dstPort : 16;
        hdr_length : 16;
        checksum : 16;
    }
}

header_type l4_t {
    fields {
        srcPort : 16;
        dstPort : 16;
    }
}

