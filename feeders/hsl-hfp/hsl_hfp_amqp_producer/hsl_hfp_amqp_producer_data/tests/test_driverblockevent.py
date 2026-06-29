"""
Test case for DriverBlockEvent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_amqp_producer_data.fi.hsl.hfp.driverblockevent import DriverBlockEvent
from typing import Any


class Test_DriverBlockEvent(unittest.TestCase):
    """
    Test case for DriverBlockEvent
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DriverBlockEvent.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DriverBlockEvent for testing
        """
        instance = DriverBlockEvent(
            oper=int(39),
            veh=int(37),
            tst='obvcranujtbirpiafeuv',
            tsi=int(89),
            operator_id='dflxkcnvrntidftaqrcw',
            vehicle_number='uqgrnrozjztbmhoeexrn',
            temporal_type=None,
            transport_mode=None,
            route_id='xbmwhcamvzvbrvzidwky',
            direction_id='bwivklwccvpaxldloinu',
            headsign='hwqfasjbjwkvyuxdpbdk',
            start_time='xtbwaxroqojuryadfyye',
            next_stop='bqbrryfzgqfeyzfkrlex',
            geohash_level='qgeoaoauhocolddppvgh',
            geohash='dyqgywevhuqvcxolcnew',
            spd=float(16.539924392464123),
            hdg=int(22),
            lat=float(98.81144156742056),
            long=float(28.22643926691032),
            acc=float(28.019485844730653),
            odo=int(56),
            drst=int(61),
            loc='gphoqbroszvealqmpxnb',
            oday='dtlwkpqwrikhudgujkwh',
            dr_type=int(71)
        )
        return instance

    
    def test_oper_property(self):
        """
        Test oper property
        """
        test_value = int(39)
        self.instance.oper = test_value
        self.assertEqual(self.instance.oper, test_value)
    
    def test_veh_property(self):
        """
        Test veh property
        """
        test_value = int(37)
        self.instance.veh = test_value
        self.assertEqual(self.instance.veh, test_value)
    
    def test_tst_property(self):
        """
        Test tst property
        """
        test_value = 'obvcranujtbirpiafeuv'
        self.instance.tst = test_value
        self.assertEqual(self.instance.tst, test_value)
    
    def test_tsi_property(self):
        """
        Test tsi property
        """
        test_value = int(89)
        self.instance.tsi = test_value
        self.assertEqual(self.instance.tsi, test_value)
    
    def test_operator_id_property(self):
        """
        Test operator_id property
        """
        test_value = 'dflxkcnvrntidftaqrcw'
        self.instance.operator_id = test_value
        self.assertEqual(self.instance.operator_id, test_value)
    
    def test_vehicle_number_property(self):
        """
        Test vehicle_number property
        """
        test_value = 'uqgrnrozjztbmhoeexrn'
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
        test_value = 'xbmwhcamvzvbrvzidwky'
        self.instance.route_id = test_value
        self.assertEqual(self.instance.route_id, test_value)
    
    def test_direction_id_property(self):
        """
        Test direction_id property
        """
        test_value = 'bwivklwccvpaxldloinu'
        self.instance.direction_id = test_value
        self.assertEqual(self.instance.direction_id, test_value)
    
    def test_headsign_property(self):
        """
        Test headsign property
        """
        test_value = 'hwqfasjbjwkvyuxdpbdk'
        self.instance.headsign = test_value
        self.assertEqual(self.instance.headsign, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'xtbwaxroqojuryadfyye'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_next_stop_property(self):
        """
        Test next_stop property
        """
        test_value = 'bqbrryfzgqfeyzfkrlex'
        self.instance.next_stop = test_value
        self.assertEqual(self.instance.next_stop, test_value)
    
    def test_geohash_level_property(self):
        """
        Test geohash_level property
        """
        test_value = 'qgeoaoauhocolddppvgh'
        self.instance.geohash_level = test_value
        self.assertEqual(self.instance.geohash_level, test_value)
    
    def test_geohash_property(self):
        """
        Test geohash property
        """
        test_value = 'dyqgywevhuqvcxolcnew'
        self.instance.geohash = test_value
        self.assertEqual(self.instance.geohash, test_value)
    
    def test_spd_property(self):
        """
        Test spd property
        """
        test_value = float(16.539924392464123)
        self.instance.spd = test_value
        self.assertEqual(self.instance.spd, test_value)
    
    def test_hdg_property(self):
        """
        Test hdg property
        """
        test_value = int(22)
        self.instance.hdg = test_value
        self.assertEqual(self.instance.hdg, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(98.81144156742056)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_long_property(self):
        """
        Test long property
        """
        test_value = float(28.22643926691032)
        self.instance.long = test_value
        self.assertEqual(self.instance.long, test_value)
    
    def test_acc_property(self):
        """
        Test acc property
        """
        test_value = float(28.019485844730653)
        self.instance.acc = test_value
        self.assertEqual(self.instance.acc, test_value)
    
    def test_odo_property(self):
        """
        Test odo property
        """
        test_value = int(56)
        self.instance.odo = test_value
        self.assertEqual(self.instance.odo, test_value)
    
    def test_drst_property(self):
        """
        Test drst property
        """
        test_value = int(61)
        self.instance.drst = test_value
        self.assertEqual(self.instance.drst, test_value)
    
    def test_loc_property(self):
        """
        Test loc property
        """
        test_value = 'gphoqbroszvealqmpxnb'
        self.instance.loc = test_value
        self.assertEqual(self.instance.loc, test_value)
    
    def test_oday_property(self):
        """
        Test oday property
        """
        test_value = 'dtlwkpqwrikhudgujkwh'
        self.instance.oday = test_value
        self.assertEqual(self.instance.oday, test_value)
    
    def test_dr_type_property(self):
        """
        Test dr_type property
        """
        test_value = int(71)
        self.instance.dr_type = test_value
        self.assertEqual(self.instance.dr_type, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DriverBlockEvent.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DriverBlockEvent.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

