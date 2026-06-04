"""
Test case for Record
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from mode_s_producer_data.mode_s.record import Record


class Test_Record(unittest.TestCase):
    """
    Test case for Record
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Record.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Record for testing
        """
        instance = Record(
            icao24='djewjfmcvvpsrgyhsszo',
            receiver_id='hikcxbjisfgsouaridzu',
            msg_type='ehvqfzdhaxjzckzgcvvd',
            ts=int(42),
            df=int(91),
            tc=int(93),
            bcode='yfnaiskzycmnaqdhsymd',
            alt=int(59),
            cs='fkfpcehajmtyulfggupz',
            sq='uecwdsbfpiopepeodvhp',
            lat=float(49.22392062335729),
            lon=float(58.08170225691427),
            spd=float(43.664052752212314),
            ang=float(69.48108086596866),
            vr=int(85),
            rssi=float(26.194829752202942)
        )
        return instance

    
    def test_icao24_property(self):
        """
        Test icao24 property
        """
        test_value = 'djewjfmcvvpsrgyhsszo'
        self.instance.icao24 = test_value
        self.assertEqual(self.instance.icao24, test_value)
    
    def test_receiver_id_property(self):
        """
        Test receiver_id property
        """
        test_value = 'hikcxbjisfgsouaridzu'
        self.instance.receiver_id = test_value
        self.assertEqual(self.instance.receiver_id, test_value)
    
    def test_msg_type_property(self):
        """
        Test msg_type property
        """
        test_value = 'ehvqfzdhaxjzckzgcvvd'
        self.instance.msg_type = test_value
        self.assertEqual(self.instance.msg_type, test_value)
    
    def test_ts_property(self):
        """
        Test ts property
        """
        test_value = int(42)
        self.instance.ts = test_value
        self.assertEqual(self.instance.ts, test_value)
    
    def test_df_property(self):
        """
        Test df property
        """
        test_value = int(91)
        self.instance.df = test_value
        self.assertEqual(self.instance.df, test_value)
    
    def test_tc_property(self):
        """
        Test tc property
        """
        test_value = int(93)
        self.instance.tc = test_value
        self.assertEqual(self.instance.tc, test_value)
    
    def test_bcode_property(self):
        """
        Test bcode property
        """
        test_value = 'yfnaiskzycmnaqdhsymd'
        self.instance.bcode = test_value
        self.assertEqual(self.instance.bcode, test_value)
    
    def test_alt_property(self):
        """
        Test alt property
        """
        test_value = int(59)
        self.instance.alt = test_value
        self.assertEqual(self.instance.alt, test_value)
    
    def test_cs_property(self):
        """
        Test cs property
        """
        test_value = 'fkfpcehajmtyulfggupz'
        self.instance.cs = test_value
        self.assertEqual(self.instance.cs, test_value)
    
    def test_sq_property(self):
        """
        Test sq property
        """
        test_value = 'uecwdsbfpiopepeodvhp'
        self.instance.sq = test_value
        self.assertEqual(self.instance.sq, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(49.22392062335729)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(58.08170225691427)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_spd_property(self):
        """
        Test spd property
        """
        test_value = float(43.664052752212314)
        self.instance.spd = test_value
        self.assertEqual(self.instance.spd, test_value)
    
    def test_ang_property(self):
        """
        Test ang property
        """
        test_value = float(69.48108086596866)
        self.instance.ang = test_value
        self.assertEqual(self.instance.ang, test_value)
    
    def test_vr_property(self):
        """
        Test vr property
        """
        test_value = int(85)
        self.instance.vr = test_value
        self.assertEqual(self.instance.vr, test_value)
    
    def test_rssi_property(self):
        """
        Test rssi property
        """
        test_value = float(26.194829752202942)
        self.instance.rssi = test_value
        self.assertEqual(self.instance.rssi, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Record.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Record.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

