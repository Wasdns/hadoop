/* TOFINO-SPECIFIC HEADER FILES */
#include "tofino/intrinsic_metadata.p4"
#include "tofino/stateful_alu_blackbox.p4"

/* HEADER AND PARSER DEFINITIONS */
#include "includes/headers.p4"
#include "includes/parser.p4"
#include "includes/routing.p4"

/* DIAGNOSIS HEADER FILES */
#include "torp.p4"

control ingress {
	/* INSERT OTHER INGRESS PROCESSING LOGICS HERE */
	torp_ingress();
	ingress_routing();
}

control egress {
	torp_egress();
}
