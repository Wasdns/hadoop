/* ROUTING DEFINITIONS */

#define PCIE_PORT 192
#define SERVER_DL13 28
#define SERVER_DL12 36
#define SERVER_DL25_1 188
#define SERVER_DL26_1 180
#define SERVER_DL25_0 172
#define SERVER_DL26_0 164
#define SERVER_DL36_0 0
#define SERVER_DL28_0 148
#define SERVER_DL28_1 156

action routing_to_DL13() {
        modify_field(ig_intr_md_for_tm.ucast_egress_port, SERVER_DL13);
}

table routing_to_DL13_tbl {
        actions { routing_to_DL13; }
        default_action : routing_to_DL13();
}

action routing_to_DL26() {
	modify_field(ig_intr_md_for_tm.ucast_egress_port, SERVER_DL26_0);
}

table routing_to_DL26_tbl {
	actions { routing_to_DL26; }
	default_action : routing_to_DL26();
}

action routing_to_DL25() {
	modify_field(ig_intr_md_for_tm.ucast_egress_port, SERVER_DL25_1);
}

table routing_to_DL25_tbl {
	actions { routing_to_DL25; }
	default_action : routing_to_DL25();
}

action routing_to_DL36() {
        modify_field(ig_intr_md_for_tm.ucast_egress_port, SERVER_DL36_0);
}

table routing_to_DL36_tbl {
        actions { routing_to_DL36; }
        default_action : routing_to_DL36();
}

action routing_to_DL28() {
        modify_field(ig_intr_md_for_tm.ucast_egress_port, SERVER_DL28_0);
}

table routing_to_DL28_tbl {
	actions { routing_to_DL28; }
	default_action : routing_to_DL28();
}

control ingress_routing {
	// routing logic:
	// request:  dl25:0 ---> switch ---> dl26:0
	// response: dl25:1 <--- switch <--- dl26:1
	if (ig_intr_md.ingress_port == SERVER_DL25_0) {
		apply(routing_to_DL26_tbl);
	} else if (ig_intr_md.ingress_port == SERVER_DL26_1 or ig_intr_md.ingress_port == SERVER_DL26_0) {
		apply(routing_to_DL25_tbl);
		//apply(routing_to_DL13_tbl);
	}
}

