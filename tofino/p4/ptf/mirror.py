import logging
import os
import pd_base_tests
import pltfm_pm_rpc
import pal_rpc
import random
import sys
import time
import unittest

from main.p4_pd_rpc.ttypes import *
from pltfm_pm_rpc.ttypes import *
from mirror_pd_rpc.ttypes import *
from pal_rpc.ttypes import *
from ptf import config
from ptf.testutils import *
from ptf.thriftutils import *
from res_pd_rpc.ttypes import *

this_dir = os.path.dirname(os.path.abspath(__file__))

# dl25:0, dl25:1, dl26:0, dl26:1
fp_ports = ["27/0", "25/0", "28/0", "26/0", "12/0", "13/0"]

def mirror_session(mir_type, mir_dir, sid, egr_port=0, egr_port_v=False,
                   egr_port_queue=0, packet_color=0, mcast_grp_a=0,
                   mcast_grp_a_v=False, mcast_grp_b=0, mcast_grp_b_v=False,
                   max_pkt_len=0, level1_mcast_hash=0, level2_mcast_hash=0,
                   cos=0, c2c=0, extract_len=0, timeout=0, int_hdr=[]):
  return MirrorSessionInfo_t(mir_type,
                             mir_dir,
                             sid,
                             egr_port,
                             egr_port_v,
                             egr_port_queue,
                             packet_color,
                             mcast_grp_a,
                             mcast_grp_a_v,
                             mcast_grp_b,
                             mcast_grp_b_v,
                             max_pkt_len,
                             level1_mcast_hash,
                             level2_mcast_hash,
                             cos,
                             c2c,
                             extract_len,
                             timeout,
                             int_hdr,
                             len(int_hdr))

class data_mirroring(pd_base_tests.ThriftInterfaceDataPlane):
    def __init__(self):
        # initialize the thrift data plane
        pd_base_tests.ThriftInterfaceDataPlane.__init__(self, ["main"])

    def cleanup_table(self, table):
        table = 'self.client.' + table
        # get entry count
        num_entries = eval(table + '_get_entry_count')(self.sess_hdl, self.dev_tgt)
        print "Number of entries : {}".format(num_entries)
        if num_entries == 0:
            return
        # get the entry handles
        hdl = eval(table + '_get_first_entry_handle')\
                (self.sess_hdl, self.dev_tgt)
        if num_entries > 1:
            hdls = eval(table + '_get_next_entry_handles')\
                (self.sess_hdl, self.dev_tgt, hdl, num_entries - 1)
            hdls.insert(0, hdl)
        else:
            hdls = [hdl]
        # delete the table entries
        for hdl in hdls:
            entry = eval(table + '_get_entry')\
                (self.sess_hdl, self.dev_tgt.dev_id, hdl, True)
            eval(table + '_table_delete_by_match_spec')\
                (self.sess_hdl, self.dev_tgt, entry.match_spec)

    def setUp(self):
        # initialize the connection
        pd_base_tests.ThriftInterfaceDataPlane.setUp(self)
        self.sess_hdl = self.conn_mgr.client_init()
        self.dev_tgt = DevTarget_t(0, hex_to_i16(0xFFFF))
        self.platform_type = "mavericks"
        board_type = self.pltfm_pm.pltfm_pm_board_type_get()
        if re.search("0x0234|0x1234|0x4234|0x5234", hex(board_type)):
            self.platform_type = "mavericks"
        elif re.search("0x2234|0x3234", hex(board_type)):
            self.platform_type = "montara"

        # get the device ports from front panel ports
        self.devPorts = []
        for fpPort in fp_ports:
            port, chnl = fpPort.split("/")
            devPort = self.pal.pal_port_front_panel_port_to_dev_port_get(0, int(port), int(chnl))
            self.devPorts.append(devPort)
        print "devports size: ", len(self.devPorts)


        if test_param_get('setup') == True or \
                (test_param_get('setup') != True and test_param_get('cleanup') != True):

            # add and enable the platform ports
            for i in self.devPorts:
               self.pal.pal_port_add(0, i,
                                     pal_port_speed_t.BF_SPEED_40G,
                                     pal_fec_type_t.BF_FEC_TYP_NONE)
               self.pal.pal_port_enable(0, i)

            print "Populating table entries"

            sid = 256
            info = mirror_session(MirrorType_e.PD_MIRROR_TYPE_NORM,
                                  Direction_e.PD_DIR_INGRESS,
                                  sid,
                                  self.devPorts[4],
                                  True)
            self.mirror.mirror_session_create(self.sess_hdl, self.dev_tgt, info)
            # self.sids.append(sid)
            # sys.stdout.flush()
            self.conn_mgr.complete_operations(self.sess_hdl)

    def runTest(self):
        print

    def tearDown(self):
        print

        if test_param_get('cleanup') == True:

            print "Cleaning up"

            # delete the programmed forward table entry
            self.cleanup_table("forward")
            # delete the platform ports
            self.conn_mgr.client_cleanup(self.sess_hdl)
            for i in self.devPorts:
                self.pal.pal_port_del(0, i)
            self.pal.pal_port_del_all(0)
