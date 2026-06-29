"""
Test case for TrafficLightEvent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_mqtt_producer_data.fi.hsl.hfp.trafficlightevent import TrafficLightEvent
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
            oper=int(26),
            veh=int(97),
            tst='vhkwceicrnherwzaacen',
            tsi=int(43),
            operator_id='ethgryefllxxwdguirbe',
            vehicle_number='fredizlusnspjscbovot',
            temporal_type=None,
            transport_mode=None,
            route_id='xdjrszeznlrekjbkggcm',
            direction_id='skkwywreigvrllkqobnm',
            headsign='fpvbyckqykapmaiwxpks',
            start_time='ouapwakdrdzspcnexxym',
            next_stop='oskiqovxgzjhtsirulpa',
            geohash_level='kclibsibyukvwfszaclp',
            geohash='nqzhrugiqtaeftjdckrq',
            desi='qssdiujbpmdhwtneenwm',
            dir='zbdmmagptmcknkztkubq',
            dl=int(19),
            oday='tlhfigknpgollvwgvphc',
            jrn=int(83),
            line=int(5),
            start='qrioyrosjnwsabmoilku',
            stop=int(0),
            route='sjnkitqdpmcgtilpkzpo',
            occu=int(60),
            spd=float(54.13089753606868),
            hdg=int(63),
            lat=float(30.05591929715834),
            long=float(38.27013990159547),
            acc=float(22.301494124758015),
            odo=int(63),
            drst=int(31),
            loc='iwaecfnqwibsdifuavbu',
            tlp_requestid=int(73),
            tlp_requesttype=None,
            tlp_prioritylevel=None,
            tlp_reason=None,
            tlp_att_seq=int(0),
            tlp_decision=None,
            sid=int(21),
            signal_groupid=int(91),
            tlp_signalgroupnbr=int(75),
            tlp_line_configid=int(2),
            tlp_point_configid=int(22),
            tlp_frequency=int(43),
            tlp_protocol='gxxaqzztbfveqlayytvx'
        )
        return instance

    
    def test_oper_property(self):
        """
        Test oper property
        """
        test_value = int(26)
        self.instance.oper = test_value
        self.assertEqual(self.instance.oper, test_value)
    
    def test_veh_property(self):
        """
        Test veh property
        """
        test_value = int(97)
        self.instance.veh = test_value
        self.assertEqual(self.instance.veh, test_value)
    
    def test_tst_property(self):
        """
        Test tst property
        """
        test_value = 'vhkwceicrnherwzaacen'
        self.instance.tst = test_value
        self.assertEqual(self.instance.tst, test_value)
    
    def test_tsi_property(self):
        """
        Test tsi property
        """
        test_value = int(43)
        self.instance.tsi = test_value
        self.assertEqual(self.instance.tsi, test_value)
    
    def test_operator_id_property(self):
        """
        Test operator_id property
        """
        test_value = 'ethgryefllxxwdguirbe'
        self.instance.operator_id = test_value
        self.assertEqual(self.instance.operator_id, test_value)
    
    def test_vehicle_number_property(self):
        """
        Test vehicle_number property
        """
        test_value = 'fredizlusnspjscbovot'
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
        test_value = 'xdjrszeznlrekjbkggcm'
        self.instance.route_id = test_value
        self.assertEqual(self.instance.route_id, test_value)
    
    def test_direction_id_property(self):
        """
        Test direction_id property
        """
        test_value = 'skkwywreigvrllkqobnm'
        self.instance.direction_id = test_value
        self.assertEqual(self.instance.direction_id, test_value)
    
    def test_headsign_property(self):
        """
        Test headsign property
        """
        test_value = 'fpvbyckqykapmaiwxpks'
        self.instance.headsign = test_value
        self.assertEqual(self.instance.headsign, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'ouapwakdrdzspcnexxym'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_next_stop_property(self):
        """
        Test next_stop property
        """
        test_value = 'oskiqovxgzjhtsirulpa'
        self.instance.next_stop = test_value
        self.assertEqual(self.instance.next_stop, test_value)
    
    def test_geohash_level_property(self):
        """
        Test geohash_level property
        """
        test_value = 'kclibsibyukvwfszaclp'
        self.instance.geohash_level = test_value
        self.assertEqual(self.instance.geohash_level, test_value)
    
    def test_geohash_property(self):
        """
        Test geohash property
        """
        test_value = 'nqzhrugiqtaeftjdckrq'
        self.instance.geohash = test_value
        self.assertEqual(self.instance.geohash, test_value)
    
    def test_desi_property(self):
        """
        Test desi property
        """
        test_value = 'qssdiujbpmdhwtneenwm'
        self.instance.desi = test_value
        self.assertEqual(self.instance.desi, test_value)
    
    def test_dir_property(self):
        """
        Test dir property
        """
        test_value = 'zbdmmagptmcknkztkubq'
        self.instance.dir = test_value
        self.assertEqual(self.instance.dir, test_value)
    
    def test_dl_property(self):
        """
        Test dl property
        """
        test_value = int(19)
        self.instance.dl = test_value
        self.assertEqual(self.instance.dl, test_value)
    
    def test_oday_property(self):
        """
        Test oday property
        """
        test_value = 'tlhfigknpgollvwgvphc'
        self.instance.oday = test_value
        self.assertEqual(self.instance.oday, test_value)
    
    def test_jrn_property(self):
        """
        Test jrn property
        """
        test_value = int(83)
        self.instance.jrn = test_value
        self.assertEqual(self.instance.jrn, test_value)
    
    def test_line_property(self):
        """
        Test line property
        """
        test_value = int(5)
        self.instance.line = test_value
        self.assertEqual(self.instance.line, test_value)
    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = 'qrioyrosjnwsabmoilku'
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_stop_property(self):
        """
        Test stop property
        """
        test_value = int(0)
        self.instance.stop = test_value
        self.assertEqual(self.instance.stop, test_value)
    
    def test_route_property(self):
        """
        Test route property
        """
        test_value = 'sjnkitqdpmcgtilpkzpo'
        self.instance.route = test_value
        self.assertEqual(self.instance.route, test_value)
    
    def test_occu_property(self):
        """
        Test occu property
        """
        test_value = int(60)
        self.instance.occu = test_value
        self.assertEqual(self.instance.occu, test_value)
    
    def test_spd_property(self):
        """
        Test spd property
        """
        test_value = float(54.13089753606868)
        self.instance.spd = test_value
        self.assertEqual(self.instance.spd, test_value)
    
    def test_hdg_property(self):
        """
        Test hdg property
        """
        test_value = int(63)
        self.instance.hdg = test_value
        self.assertEqual(self.instance.hdg, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(30.05591929715834)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_long_property(self):
        """
        Test long property
        """
        test_value = float(38.27013990159547)
        self.instance.long = test_value
        self.assertEqual(self.instance.long, test_value)
    
    def test_acc_property(self):
        """
        Test acc property
        """
        test_value = float(22.301494124758015)
        self.instance.acc = test_value
        self.assertEqual(self.instance.acc, test_value)
    
    def test_odo_property(self):
        """
        Test odo property
        """
        test_value = int(63)
        self.instance.odo = test_value
        self.assertEqual(self.instance.odo, test_value)
    
    def test_drst_property(self):
        """
        Test drst property
        """
        test_value = int(31)
        self.instance.drst = test_value
        self.assertEqual(self.instance.drst, test_value)
    
    def test_loc_property(self):
        """
        Test loc property
        """
        test_value = 'iwaecfnqwibsdifuavbu'
        self.instance.loc = test_value
        self.assertEqual(self.instance.loc, test_value)
    
    def test_tlp_requestid_property(self):
        """
        Test tlp_requestid property
        """
        test_value = int(73)
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
        test_value = int(0)
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
        test_value = int(21)
        self.instance.sid = test_value
        self.assertEqual(self.instance.sid, test_value)
    
    def test_signal_groupid_property(self):
        """
        Test signal_groupid property
        """
        test_value = int(91)
        self.instance.signal_groupid = test_value
        self.assertEqual(self.instance.signal_groupid, test_value)
    
    def test_tlp_signalgroupnbr_property(self):
        """
        Test tlp_signalgroupnbr property
        """
        test_value = int(75)
        self.instance.tlp_signalgroupnbr = test_value
        self.assertEqual(self.instance.tlp_signalgroupnbr, test_value)
    
    def test_tlp_line_configid_property(self):
        """
        Test tlp_line_configid property
        """
        test_value = int(2)
        self.instance.tlp_line_configid = test_value
        self.assertEqual(self.instance.tlp_line_configid, test_value)
    
    def test_tlp_point_configid_property(self):
        """
        Test tlp_point_configid property
        """
        test_value = int(22)
        self.instance.tlp_point_configid = test_value
        self.assertEqual(self.instance.tlp_point_configid, test_value)
    
    def test_tlp_frequency_property(self):
        """
        Test tlp_frequency property
        """
        test_value = int(43)
        self.instance.tlp_frequency = test_value
        self.assertEqual(self.instance.tlp_frequency, test_value)
    
    def test_tlp_protocol_property(self):
        """
        Test tlp_protocol property
        """
        test_value = 'gxxaqzztbfveqlayytvx'
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

