"""
Test case for VehicleEvent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_mqtt_producer_data.fi.hsl.hfp.vehicleevent import VehicleEvent
from typing import Any


class Test_VehicleEvent(unittest.TestCase):
    """
    Test case for VehicleEvent
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VehicleEvent.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VehicleEvent for testing
        """
        instance = VehicleEvent(
            oper=int(93),
            veh=int(9),
            tst='sivvexlmvyxlvfpzigwh',
            tsi=int(40),
            operator_id='knbwpdjssevwbskbyssb',
            vehicle_number='eacmqaqmszouvksisecw',
            temporal_type=None,
            transport_mode=None,
            route_id='umcoeavbgldqbmxcgdlc',
            direction_id='irterqkaptzapbsimlwa',
            headsign='ywtpnwbzpdzkdqssgbkh',
            start_time='fhulohxiyxycuoifiptv',
            next_stop='ciotnwhkzwajwtdbzdok',
            geohash_level='bknjjsvogopdgomxlldp',
            geohash='dmpefwywtfiliptjylbj',
            desi='towqtocgrpjhdtcpxrzs',
            dir='ywehginzspytffaotahk',
            dl=int(75),
            oday='kwoowqvcnvsybxnppcix',
            jrn=int(9),
            line=int(68),
            start='tguonatnutxtcmbfxvhg',
            stop=int(38),
            route='tevaqnarnvnlkavpesho',
            occu=int(94),
            seq=int(4),
            label='pnjdahumqpgltxcdehay',
            spd=float(27.666501329514137),
            hdg=int(69),
            lat=float(60.34994618344268),
            long=float(37.13210585195509),
            acc=float(9.036410874969958),
            odo=int(55),
            drst=int(25),
            loc='elpyqmchxvtchopmmzmn',
            ttarr='tlqxhzpaiuelmgwgehbi',
            ttdep='sklbogkmwgbpkrhpyzfg',
            dr_type=int(66)
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
        test_value = int(9)
        self.instance.veh = test_value
        self.assertEqual(self.instance.veh, test_value)
    
    def test_tst_property(self):
        """
        Test tst property
        """
        test_value = 'sivvexlmvyxlvfpzigwh'
        self.instance.tst = test_value
        self.assertEqual(self.instance.tst, test_value)
    
    def test_tsi_property(self):
        """
        Test tsi property
        """
        test_value = int(40)
        self.instance.tsi = test_value
        self.assertEqual(self.instance.tsi, test_value)
    
    def test_operator_id_property(self):
        """
        Test operator_id property
        """
        test_value = 'knbwpdjssevwbskbyssb'
        self.instance.operator_id = test_value
        self.assertEqual(self.instance.operator_id, test_value)
    
    def test_vehicle_number_property(self):
        """
        Test vehicle_number property
        """
        test_value = 'eacmqaqmszouvksisecw'
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
        test_value = 'umcoeavbgldqbmxcgdlc'
        self.instance.route_id = test_value
        self.assertEqual(self.instance.route_id, test_value)
    
    def test_direction_id_property(self):
        """
        Test direction_id property
        """
        test_value = 'irterqkaptzapbsimlwa'
        self.instance.direction_id = test_value
        self.assertEqual(self.instance.direction_id, test_value)
    
    def test_headsign_property(self):
        """
        Test headsign property
        """
        test_value = 'ywtpnwbzpdzkdqssgbkh'
        self.instance.headsign = test_value
        self.assertEqual(self.instance.headsign, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'fhulohxiyxycuoifiptv'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_next_stop_property(self):
        """
        Test next_stop property
        """
        test_value = 'ciotnwhkzwajwtdbzdok'
        self.instance.next_stop = test_value
        self.assertEqual(self.instance.next_stop, test_value)
    
    def test_geohash_level_property(self):
        """
        Test geohash_level property
        """
        test_value = 'bknjjsvogopdgomxlldp'
        self.instance.geohash_level = test_value
        self.assertEqual(self.instance.geohash_level, test_value)
    
    def test_geohash_property(self):
        """
        Test geohash property
        """
        test_value = 'dmpefwywtfiliptjylbj'
        self.instance.geohash = test_value
        self.assertEqual(self.instance.geohash, test_value)
    
    def test_desi_property(self):
        """
        Test desi property
        """
        test_value = 'towqtocgrpjhdtcpxrzs'
        self.instance.desi = test_value
        self.assertEqual(self.instance.desi, test_value)
    
    def test_dir_property(self):
        """
        Test dir property
        """
        test_value = 'ywehginzspytffaotahk'
        self.instance.dir = test_value
        self.assertEqual(self.instance.dir, test_value)
    
    def test_dl_property(self):
        """
        Test dl property
        """
        test_value = int(75)
        self.instance.dl = test_value
        self.assertEqual(self.instance.dl, test_value)
    
    def test_oday_property(self):
        """
        Test oday property
        """
        test_value = 'kwoowqvcnvsybxnppcix'
        self.instance.oday = test_value
        self.assertEqual(self.instance.oday, test_value)
    
    def test_jrn_property(self):
        """
        Test jrn property
        """
        test_value = int(9)
        self.instance.jrn = test_value
        self.assertEqual(self.instance.jrn, test_value)
    
    def test_line_property(self):
        """
        Test line property
        """
        test_value = int(68)
        self.instance.line = test_value
        self.assertEqual(self.instance.line, test_value)
    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = 'tguonatnutxtcmbfxvhg'
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_stop_property(self):
        """
        Test stop property
        """
        test_value = int(38)
        self.instance.stop = test_value
        self.assertEqual(self.instance.stop, test_value)
    
    def test_route_property(self):
        """
        Test route property
        """
        test_value = 'tevaqnarnvnlkavpesho'
        self.instance.route = test_value
        self.assertEqual(self.instance.route, test_value)
    
    def test_occu_property(self):
        """
        Test occu property
        """
        test_value = int(94)
        self.instance.occu = test_value
        self.assertEqual(self.instance.occu, test_value)
    
    def test_seq_property(self):
        """
        Test seq property
        """
        test_value = int(4)
        self.instance.seq = test_value
        self.assertEqual(self.instance.seq, test_value)
    
    def test_label_property(self):
        """
        Test label property
        """
        test_value = 'pnjdahumqpgltxcdehay'
        self.instance.label = test_value
        self.assertEqual(self.instance.label, test_value)
    
    def test_spd_property(self):
        """
        Test spd property
        """
        test_value = float(27.666501329514137)
        self.instance.spd = test_value
        self.assertEqual(self.instance.spd, test_value)
    
    def test_hdg_property(self):
        """
        Test hdg property
        """
        test_value = int(69)
        self.instance.hdg = test_value
        self.assertEqual(self.instance.hdg, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(60.34994618344268)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_long_property(self):
        """
        Test long property
        """
        test_value = float(37.13210585195509)
        self.instance.long = test_value
        self.assertEqual(self.instance.long, test_value)
    
    def test_acc_property(self):
        """
        Test acc property
        """
        test_value = float(9.036410874969958)
        self.instance.acc = test_value
        self.assertEqual(self.instance.acc, test_value)
    
    def test_odo_property(self):
        """
        Test odo property
        """
        test_value = int(55)
        self.instance.odo = test_value
        self.assertEqual(self.instance.odo, test_value)
    
    def test_drst_property(self):
        """
        Test drst property
        """
        test_value = int(25)
        self.instance.drst = test_value
        self.assertEqual(self.instance.drst, test_value)
    
    def test_loc_property(self):
        """
        Test loc property
        """
        test_value = 'elpyqmchxvtchopmmzmn'
        self.instance.loc = test_value
        self.assertEqual(self.instance.loc, test_value)
    
    def test_ttarr_property(self):
        """
        Test ttarr property
        """
        test_value = 'tlqxhzpaiuelmgwgehbi'
        self.instance.ttarr = test_value
        self.assertEqual(self.instance.ttarr, test_value)
    
    def test_ttdep_property(self):
        """
        Test ttdep property
        """
        test_value = 'sklbogkmwgbpkrhpyzfg'
        self.instance.ttdep = test_value
        self.assertEqual(self.instance.ttdep, test_value)
    
    def test_dr_type_property(self):
        """
        Test dr_type property
        """
        test_value = int(66)
        self.instance.dr_type = test_value
        self.assertEqual(self.instance.dr_type, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VehicleEvent.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VehicleEvent.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

