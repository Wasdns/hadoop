header_type torp_metadata_t {
	fields {
		srcIP : 32;
		dstIP : 32;
		proto : 8;
		srcPort : 16;
		dstPort : 16;
	}
}
metadata torp_metadata_t torp_md;

/* ADD TIMESTAMP INFORMATION (IN&OUT TIMESTAMP) TO DIAGNOSIS HEADER */

action add_info() {
	modify_field(torp_md.srcIP, ipv4.srcAddr);
	modify_field(torp_md.dstIP, ipv4.dstAddr);
	modify_field(torp_md.proto, ipv4.protocol);
	modify_field(torp_md.srcPort, tcp.srcPort);
	modify_field(torp_md.dstPort, tcp.dstPort);
}

table add_info_tbl {
	actions { add_info; }
	default_action : add_info();
}

/* MIRRORING DEFINITIONS */

// Here, we need to add a rule that associates the mirroring egress port with the session ID
#define SESSION_ID 256

field_list req_rsp_mirror_list {
	torp_md.srcIP;
	torp_md.dstIP;
	torp_md.proto;
	torp_md.srcPort;
	torp_md.dstPort;
}

action req_rsp_pkt_mirror() {
	clone_ingress_pkt_to_egress(SESSION_ID, req_rsp_mirror_list); 
}

table req_rsp_pkt_mirror_tbl {
	actions { req_rsp_pkt_mirror; }
	default_action : req_rsp_pkt_mirror();
}

action add_diagnosis_hdr() {
	add_header(diagnosis_hdr);
	modify_field(diagnosis_hdr.srcIP, torp_md.srcIP);
	modify_field(diagnosis_hdr.dstIP, torp_md.dstIP);
	modify_field(diagnosis_hdr.proto, torp_md.proto);
	modify_field(diagnosis_hdr.srcPort, torp_md.srcPort);
	modify_field(diagnosis_hdr.dstPort, torp_md.dstPort);
	modify_field(ethernet.etherType, 0xfff);
	remove_header(ipv4);
	remove_header(tcp);
	remove_header(udp);
}

table add_diagnosis_hdr_tbl {
	actions { add_diagnosis_hdr; }
	default_action : add_diagnosis_hdr();
}

/* CONTROL FLOWS */

control torp_ingress 
{
	apply(add_info_tbl);
	apply(req_rsp_pkt_mirror_tbl);
}

control torp_egress 
{
	if (eg_intr_md_from_parser_aux.clone_src == 0) {
		// do nothing
	} else {
		// add five tuple information
		apply(add_diagnosis_hdr_tbl);
	}
}


