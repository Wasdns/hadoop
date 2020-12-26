# This file is to be kept in precise sync with constants.p4

#############################################################
# Parser hardware error codes
parser_error_constants = {
    "PARSER_ERROR_OK": 0x0000,
    "PARSER_ERROR_NO_TCAM": 0x0001,
    "PARSER_ERROR_PARTIAL_HDR": 0x0002,
    "PARSER_ERROR_CTR_RANGE": 0x0004,
    "PARSER_ERROR_TIMEOUT_USER": 0x0008,
    "PARSER_ERROR_TIMEOUT_HW": 0x0010,
    "PARSER_ERROR_SRC_EXT": 0x0020,
    "PARSER_ERROR_DST_CONT": 0x0040,
    "PARSER_ERROR_PHV_OWNER": 0x0080,
    "PARSER_ERROR_MULTIWRITE": 0x0100,
    "PARSER_ERROR_ARAM_SBE": 0x0200,
    "PARSER_ERROR_ARAM_MBE": 0x0400,
    "PARSER_ERROR_FCS": 0x800,
    "PARSER_ERROR_CSUM": 0x1000,
    "PARSER_ERROR_ARRAY_OOB": 0xC000,
}
#############################################################


#############################################################
# Digest receivers
digest_constants = {
    "FLOW_LRN_DIGEST_RCVR": 0,

    "RECIRCULATE_DIGEST_RCVR": 90,
    "RESUBMIT_DIGEST_RCVR": 91,
    "CLONE_I2I_DIGEST_RCVR": 92,
    "CLONE_E2I_DIGEST_RCVR": 93,
    "CLONE_I2E_DIGEST_RCVR": 94,
    "CLONE_E2E_DIGEST_RCVR": 95,
}

# Dictionary that maps digest receiver name to tuple consisting of
# how many of the PHV container bits to set and the container lsb position to start writing the value
digest_phv_container_bits_to_set_properties = {"FLOW_LRN_DIGEST_RCVR": (3, 0),
                                               "CLONE_I2E_DIGEST_RCVR": (5, 0),
                                               "CLONE_E2E_DIGEST_RCVR": (5, 0),
                                               "RESUBMIT_DIGEST_RCVR": (3, 0)}

#############################################################


#############################################################
# Clone soruces
# (to be used with eg_intr_md_from_parser_aux.clone_src)
clone_sources = {
    "NOT_CLONED": 0,
    "CLONED_FROM_INGRESS": 1,
    "CLONED_FROM_EGRESS": 3,
    "COALESCED": 5,
}
#############################################################

#############################################################
# Parser priorities

parser_pri = {
    "PARSER_DEF_PRI" : 0,
    "PARSER_THRESH_PRI" : 3
}
