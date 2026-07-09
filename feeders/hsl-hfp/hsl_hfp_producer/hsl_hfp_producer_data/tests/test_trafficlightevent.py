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
            oper=int(73),
            veh=int(80),
            tst='ymmwfdhvsltiutynipmr',
            tsi=int(59),
            operator_id='wjwticmopuwlcmzqnvvs',
            vehicle_number='qyhfdjzjfhkqfhfqhkfk',
            temporal_type=None,
            transport_mode=None,
            route_id='oevqejfnihnhivtunppl',
            direction_id='bisqsximazsegiyclnth',
            headsign='kvadhdphpxyabqdtjvwu',
            start_time='oeivyavxkossvrvwqmjr',
            next_stop='wfnqrpmvnrqvkpvaizph',
            geohash_level='ayzgerucjthvslzlljos',
            geohash='elngpzqjpfjuwtybgoxu',
            desi='oxogazihnumrbskzvrtd',
            dir=None,
            dl=int(15),
            oday='xaucasvverhxzuyfqjed',
            jrn=int(79),
            line=int(62),
            start='tdyuphwreznmavuxfvcq',
            stop=int(87),
            route='fgmhdwpaeucqgxsfkapo',
            occu=int(14),
            spd=float(44.036625108439765),
            hdg=int(58),
            lat=float(98.9524966578608),
            long=float(40.21201616838154),
            acc=float(36.05886398084134),
            odo=int(98),
            drst=int(53),
            loc=None,
            tlp_requestid=int(37),
            tlp_requesttype=None,
            tlp_prioritylevel=None,
            tlp_reason=None,
            tlp_att_seq=int(2),
            tlp_decision=None,
            sid=int(51),
            signal_groupid=int(95),
            tlp_signalgroupnbr=int(96),
            tlp_line_configid=int(65),
            tlp_point_configid=int(23),
            tlp_frequency=int(64),
            tlp_protocol=None
        )
        return instance

    
    def test_oper_property(self):
        """
        Test oper property
        """
        test_value = int(73)
        self.instance.oper = test_value
        self.assertEqual(self.instance.oper, test_value)
    
    def test_veh_property(self):
        """
        Test veh property
        """
        test_value = int(80)
        self.instance.veh = test_value
        self.assertEqual(self.instance.veh, test_value)
    
    def test_tst_property(self):
        """
        Test tst property
        """
        test_value = 'ymmwfdhvsltiutynipmr'
        self.instance.tst = test_value
        self.assertEqual(self.instance.tst, test_value)
    
    def test_tsi_property(self):
        """
        Test tsi property
        """
        test_value = int(59)
        self.instance.tsi = test_value
        self.assertEqual(self.instance.tsi, test_value)
    
    def test_operator_id_property(self):
        """
        Test operator_id property
        """
        test_value = 'wjwticmopuwlcmzqnvvs'
        self.instance.operator_id = test_value
        self.assertEqual(self.instance.operator_id, test_value)
    
    def test_vehicle_number_property(self):
        """
        Test vehicle_number property
        """
        test_value = 'qyhfdjzjfhkqfhfqhkfk'
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
        test_value = 'oevqejfnihnhivtunppl'
        self.instance.route_id = test_value
        self.assertEqual(self.instance.route_id, test_value)
    
    def test_direction_id_property(self):
        """
        Test direction_id property
        """
        test_value = 'bisqsximazsegiyclnth'
        self.instance.direction_id = test_value
        self.assertEqual(self.instance.direction_id, test_value)
    
    def test_headsign_property(self):
        """
        Test headsign property
        """
        test_value = 'kvadhdphpxyabqdtjvwu'
        self.instance.headsign = test_value
        self.assertEqual(self.instance.headsign, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'oeivyavxkossvrvwqmjr'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_next_stop_property(self):
        """
        Test next_stop property
        """
        test_value = 'wfnqrpmvnrqvkpvaizph'
        self.instance.next_stop = test_value
        self.assertEqual(self.instance.next_stop, test_value)
    
    def test_geohash_level_property(self):
        """
        Test geohash_level property
        """
        test_value = 'ayzgerucjthvslzlljos'
        self.instance.geohash_level = test_value
        self.assertEqual(self.instance.geohash_level, test_value)
    
    def test_geohash_property(self):
        """
        Test geohash property
        """
        test_value = 'elngpzqjpfjuwtybgoxu'
        self.instance.geohash = test_value
        self.assertEqual(self.instance.geohash, test_value)
    
    def test_desi_property(self):
        """
        Test desi property
        """
        test_value = 'oxogazihnumrbskzvrtd'
        self.instance.desi = test_value
        self.assertEqual(self.instance.desi, test_value)
    
    def test_dir_property(self):
        """
        Test dir property
        """
        test_value = None
        self.instance.dir = test_value
        self.assertEqual(self.instance.dir, test_value)
    
    def test_dl_property(self):
        """
        Test dl property
        """
        test_value = int(15)
        self.instance.dl = test_value
        self.assertEqual(self.instance.dl, test_value)
    
    def test_oday_property(self):
        """
        Test oday property
        """
        test_value = 'xaucasvverhxzuyfqjed'
        self.instance.oday = test_value
        self.assertEqual(self.instance.oday, test_value)
    
    def test_jrn_property(self):
        """
        Test jrn property
        """
        test_value = int(79)
        self.instance.jrn = test_value
        self.assertEqual(self.instance.jrn, test_value)
    
    def test_line_property(self):
        """
        Test line property
        """
        test_value = int(62)
        self.instance.line = test_value
        self.assertEqual(self.instance.line, test_value)
    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = 'tdyuphwreznmavuxfvcq'
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_stop_property(self):
        """
        Test stop property
        """
        test_value = int(87)
        self.instance.stop = test_value
        self.assertEqual(self.instance.stop, test_value)
    
    def test_route_property(self):
        """
        Test route property
        """
        test_value = 'fgmhdwpaeucqgxsfkapo'
        self.instance.route = test_value
        self.assertEqual(self.instance.route, test_value)
    
    def test_occu_property(self):
        """
        Test occu property
        """
        test_value = int(14)
        self.instance.occu = test_value
        self.assertEqual(self.instance.occu, test_value)
    
    def test_spd_property(self):
        """
        Test spd property
        """
        test_value = float(44.036625108439765)
        self.instance.spd = test_value
        self.assertEqual(self.instance.spd, test_value)
    
    def test_hdg_property(self):
        """
        Test hdg property
        """
        test_value = int(58)
        self.instance.hdg = test_value
        self.assertEqual(self.instance.hdg, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(98.9524966578608)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_long_property(self):
        """
        Test long property
        """
        test_value = float(40.21201616838154)
        self.instance.long = test_value
        self.assertEqual(self.instance.long, test_value)
    
    def test_acc_property(self):
        """
        Test acc property
        """
        test_value = float(36.05886398084134)
        self.instance.acc = test_value
        self.assertEqual(self.instance.acc, test_value)
    
    def test_odo_property(self):
        """
        Test odo property
        """
        test_value = int(98)
        self.instance.odo = test_value
        self.assertEqual(self.instance.odo, test_value)
    
    def test_drst_property(self):
        """
        Test drst property
        """
        test_value = int(53)
        self.instance.drst = test_value
        self.assertEqual(self.instance.drst, test_value)
    
    def test_loc_property(self):
        """
        Test loc property
        """
        test_value = None
        self.instance.loc = test_value
        self.assertEqual(self.instance.loc, test_value)
    
    def test_tlp_requestid_property(self):
        """
        Test tlp_requestid property
        """
        test_value = int(37)
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
        test_value = int(2)
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
        test_value = int(51)
        self.instance.sid = test_value
        self.assertEqual(self.instance.sid, test_value)
    
    def test_signal_groupid_property(self):
        """
        Test signal_groupid property
        """
        test_value = int(95)
        self.instance.signal_groupid = test_value
        self.assertEqual(self.instance.signal_groupid, test_value)
    
    def test_tlp_signalgroupnbr_property(self):
        """
        Test tlp_signalgroupnbr property
        """
        test_value = int(96)
        self.instance.tlp_signalgroupnbr = test_value
        self.assertEqual(self.instance.tlp_signalgroupnbr, test_value)
    
    def test_tlp_line_configid_property(self):
        """
        Test tlp_line_configid property
        """
        test_value = int(65)
        self.instance.tlp_line_configid = test_value
        self.assertEqual(self.instance.tlp_line_configid, test_value)
    
    def test_tlp_point_configid_property(self):
        """
        Test tlp_point_configid property
        """
        test_value = int(23)
        self.instance.tlp_point_configid = test_value
        self.assertEqual(self.instance.tlp_point_configid, test_value)
    
    def test_tlp_frequency_property(self):
        """
        Test tlp_frequency property
        """
        test_value = int(64)
        self.instance.tlp_frequency = test_value
        self.assertEqual(self.instance.tlp_frequency, test_value)
    
    def test_tlp_protocol_property(self):
        """
        Test tlp_protocol property
        """
        test_value = None
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

