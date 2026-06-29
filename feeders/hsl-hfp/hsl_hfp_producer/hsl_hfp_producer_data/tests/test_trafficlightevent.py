"""
Test case for TrafficLightEvent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_producer_data.fi.hsl.hfp.trafficlightevent import TrafficLightEvent
from typing import Any


class Test_TrafficLightEvent(unittest.TestCase):
    """
    Test case for TrafficLightEvent
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TrafficLightEvent.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TrafficLightEvent for testing
        """
        instance = TrafficLightEvent(
            oper=int(93),
            veh=int(84),
            tst='rbqgbpprhohuzskcpsxc',
            tsi=int(52),
            operator_id='euzesezrpyywgpwmpvtg',
            vehicle_number='bjqadnikbkljwrkxhovn',
            temporal_type=None,
            transport_mode=None,
            route_id='iuwwlittjsmeffbvcqva',
            direction_id='lbbwsouzhbzrtzlwezqa',
            headsign='zkwbsxlrsqfeslmlwbhq',
            start_time='fsqaytbhaphfdiqmbbox',
            next_stop='bzqmfybinogkxuqbngft',
            geohash_level='mkzduzudgexcvjzxfjxp',
            geohash='danjcvmiabkemthsihrg',
            desi='edotcpwwlobvubwxqqra',
            dir='zwlftkcozqnlonzqhlhl',
            dl=int(13),
            oday='eblwthyjzdugdfspzkmg',
            jrn=int(11),
            line=int(100),
            start='bbbpfaufmujfwahligev',
            stop=int(11),
            route='mbhwdqhqfnrckmpbkbvg',
            occu=int(61),
            spd=float(82.13116049264633),
            hdg=int(40),
            lat=float(76.12836445370715),
            long=float(72.12763104647497),
            acc=float(93.93436013265197),
            odo=int(36),
            drst=int(19),
            loc='serzuwihrauxcyrphais',
            tlp_requestid=int(53),
            tlp_requesttype=None,
            tlp_prioritylevel=None,
            tlp_reason=None,
            tlp_att_seq=int(47),
            tlp_decision=None,
            sid=int(56),
            signal_groupid=int(98),
            tlp_signalgroupnbr=int(76),
            tlp_line_configid=int(17),
            tlp_point_configid=int(88),
            tlp_frequency=int(67),
            tlp_protocol='jrksflwnzaogslgbqbtv'
        )
        return instance

    
    def test_oper_property(self):
        """
        Test oper property
        """
        test_value = int(93)
        self.instance.oper = test_value
        self.assertEqual(self.instance.oper, test_value)
    
    def test_veh_property(self):
        """
        Test veh property
        """
        test_value = int(84)
        self.instance.veh = test_value
        self.assertEqual(self.instance.veh, test_value)
    
    def test_tst_property(self):
        """
        Test tst property
        """
        test_value = 'rbqgbpprhohuzskcpsxc'
        self.instance.tst = test_value
        self.assertEqual(self.instance.tst, test_value)
    
    def test_tsi_property(self):
        """
        Test tsi property
        """
        test_value = int(52)
        self.instance.tsi = test_value
        self.assertEqual(self.instance.tsi, test_value)
    
    def test_operator_id_property(self):
        """
        Test operator_id property
        """
        test_value = 'euzesezrpyywgpwmpvtg'
        self.instance.operator_id = test_value
        self.assertEqual(self.instance.operator_id, test_value)
    
    def test_vehicle_number_property(self):
        """
        Test vehicle_number property
        """
        test_value = 'bjqadnikbkljwrkxhovn'
        self.instance.vehicle_number = test_value
        self.assertEqual(self.instance.vehicle_number, test_value)
    
    def test_temporal_type_property(self):
        """
        Test temporal_type property
        """
        test_value = None
        self.instance.temporal_type = test_value
        self.assertEqual(self.instance.temporal_type, test_value)
    
    def test_transport_mode_property(self):
        """
        Test transport_mode property
        """
        test_value = None
        self.instance.transport_mode = test_value
        self.assertEqual(self.instance.transport_mode, test_value)
    
    def test_route_id_property(self):
        """
        Test route_id property
        """
        test_value = 'iuwwlittjsmeffbvcqva'
        self.instance.route_id = test_value
        self.assertEqual(self.instance.route_id, test_value)
    
    def test_direction_id_property(self):
        """
        Test direction_id property
        """
        test_value = 'lbbwsouzhbzrtzlwezqa'
        self.instance.direction_id = test_value
        self.assertEqual(self.instance.direction_id, test_value)
    
    def test_headsign_property(self):
        """
        Test headsign property
        """
        test_value = 'zkwbsxlrsqfeslmlwbhq'
        self.instance.headsign = test_value
        self.assertEqual(self.instance.headsign, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'fsqaytbhaphfdiqmbbox'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_next_stop_property(self):
        """
        Test next_stop property
        """
        test_value = 'bzqmfybinogkxuqbngft'
        self.instance.next_stop = test_value
        self.assertEqual(self.instance.next_stop, test_value)
    
    def test_geohash_level_property(self):
        """
        Test geohash_level property
        """
        test_value = 'mkzduzudgexcvjzxfjxp'
        self.instance.geohash_level = test_value
        self.assertEqual(self.instance.geohash_level, test_value)
    
    def test_geohash_property(self):
        """
        Test geohash property
        """
        test_value = 'danjcvmiabkemthsihrg'
        self.instance.geohash = test_value
        self.assertEqual(self.instance.geohash, test_value)
    
    def test_desi_property(self):
        """
        Test desi property
        """
        test_value = 'edotcpwwlobvubwxqqra'
        self.instance.desi = test_value
        self.assertEqual(self.instance.desi, test_value)
    
    def test_dir_property(self):
        """
        Test dir property
        """
        test_value = 'zwlftkcozqnlonzqhlhl'
        self.instance.dir = test_value
        self.assertEqual(self.instance.dir, test_value)
    
    def test_dl_property(self):
        """
        Test dl property
        """
        test_value = int(13)
        self.instance.dl = test_value
        self.assertEqual(self.instance.dl, test_value)
    
    def test_oday_property(self):
        """
        Test oday property
        """
        test_value = 'eblwthyjzdugdfspzkmg'
        self.instance.oday = test_value
        self.assertEqual(self.instance.oday, test_value)
    
    def test_jrn_property(self):
        """
        Test jrn property
        """
        test_value = int(11)
        self.instance.jrn = test_value
        self.assertEqual(self.instance.jrn, test_value)
    
    def test_line_property(self):
        """
        Test line property
        """
        test_value = int(100)
        self.instance.line = test_value
        self.assertEqual(self.instance.line, test_value)
    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = 'bbbpfaufmujfwahligev'
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_stop_property(self):
        """
        Test stop property
        """
        test_value = int(11)
        self.instance.stop = test_value
        self.assertEqual(self.instance.stop, test_value)
    
    def test_route_property(self):
        """
        Test route property
        """
        test_value = 'mbhwdqhqfnrckmpbkbvg'
        self.instance.route = test_value
        self.assertEqual(self.instance.route, test_value)
    
    def test_occu_property(self):
        """
        Test occu property
        """
        test_value = int(61)
        self.instance.occu = test_value
        self.assertEqual(self.instance.occu, test_value)
    
    def test_spd_property(self):
        """
        Test spd property
        """
        test_value = float(82.13116049264633)
        self.instance.spd = test_value
        self.assertEqual(self.instance.spd, test_value)
    
    def test_hdg_property(self):
        """
        Test hdg property
        """
        test_value = int(40)
        self.instance.hdg = test_value
        self.assertEqual(self.instance.hdg, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(76.12836445370715)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_long_property(self):
        """
        Test long property
        """
        test_value = float(72.12763104647497)
        self.instance.long = test_value
        self.assertEqual(self.instance.long, test_value)
    
    def test_acc_property(self):
        """
        Test acc property
        """
        test_value = float(93.93436013265197)
        self.instance.acc = test_value
        self.assertEqual(self.instance.acc, test_value)
    
    def test_odo_property(self):
        """
        Test odo property
        """
        test_value = int(36)
        self.instance.odo = test_value
        self.assertEqual(self.instance.odo, test_value)
    
    def test_drst_property(self):
        """
        Test drst property
        """
        test_value = int(19)
        self.instance.drst = test_value
        self.assertEqual(self.instance.drst, test_value)
    
    def test_loc_property(self):
        """
        Test loc property
        """
        test_value = 'serzuwihrauxcyrphais'
        self.instance.loc = test_value
        self.assertEqual(self.instance.loc, test_value)
    
    def test_tlp_requestid_property(self):
        """
        Test tlp_requestid property
        """
        test_value = int(53)
        self.instance.tlp_requestid = test_value
        self.assertEqual(self.instance.tlp_requestid, test_value)
    
    def test_tlp_requesttype_property(self):
        """
        Test tlp_requesttype property
        """
        test_value = None
        self.instance.tlp_requesttype = test_value
        self.assertEqual(self.instance.tlp_requesttype, test_value)
    
    def test_tlp_prioritylevel_property(self):
        """
        Test tlp_prioritylevel property
        """
        test_value = None
        self.instance.tlp_prioritylevel = test_value
        self.assertEqual(self.instance.tlp_prioritylevel, test_value)
    
    def test_tlp_reason_property(self):
        """
        Test tlp_reason property
        """
        test_value = None
        self.instance.tlp_reason = test_value
        self.assertEqual(self.instance.tlp_reason, test_value)
    
    def test_tlp_att_seq_property(self):
        """
        Test tlp_att_seq property
        """
        test_value = int(47)
        self.instance.tlp_att_seq = test_value
        self.assertEqual(self.instance.tlp_att_seq, test_value)
    
    def test_tlp_decision_property(self):
        """
        Test tlp_decision property
        """
        test_value = None
        self.instance.tlp_decision = test_value
        self.assertEqual(self.instance.tlp_decision, test_value)
    
    def test_sid_property(self):
        """
        Test sid property
        """
        test_value = int(56)
        self.instance.sid = test_value
        self.assertEqual(self.instance.sid, test_value)
    
    def test_signal_groupid_property(self):
        """
        Test signal_groupid property
        """
        test_value = int(98)
        self.instance.signal_groupid = test_value
        self.assertEqual(self.instance.signal_groupid, test_value)
    
    def test_tlp_signalgroupnbr_property(self):
        """
        Test tlp_signalgroupnbr property
        """
        test_value = int(76)
        self.instance.tlp_signalgroupnbr = test_value
        self.assertEqual(self.instance.tlp_signalgroupnbr, test_value)
    
    def test_tlp_line_configid_property(self):
        """
        Test tlp_line_configid property
        """
        test_value = int(17)
        self.instance.tlp_line_configid = test_value
        self.assertEqual(self.instance.tlp_line_configid, test_value)
    
    def test_tlp_point_configid_property(self):
        """
        Test tlp_point_configid property
        """
        test_value = int(88)
        self.instance.tlp_point_configid = test_value
        self.assertEqual(self.instance.tlp_point_configid, test_value)
    
    def test_tlp_frequency_property(self):
        """
        Test tlp_frequency property
        """
        test_value = int(67)
        self.instance.tlp_frequency = test_value
        self.assertEqual(self.instance.tlp_frequency, test_value)
    
    def test_tlp_protocol_property(self):
        """
        Test tlp_protocol property
        """
        test_value = 'jrksflwnzaogslgbqbtv'
        self.instance.tlp_protocol = test_value
        self.assertEqual(self.instance.tlp_protocol, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TrafficLightEvent.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TrafficLightEvent.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

