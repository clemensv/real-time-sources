"""
Test case for Record
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from mode_s_amqp_producer_data.mode_s.record import Record


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
            icao24='ddsovwhourmbuqnyyruv',
            receiver_id='rbcvzbyhryxufbnanpfo',
            msg_type='hlgwxujwwedhyozepnkr',
            ts=int(74),
            df=int(49),
            tc=int(11),
            bcode='zjpalbxtscxsnnjetxyk',
            alt=int(72),
            cs='zmncsiyjwlmkvgahwnjv',
            sq='gedgnyhywwbgbohaaeam',
            lat=float(70.76614598548544),
            lon=float(58.267423003742216),
            spd=float(11.856856640287516),
            ang=float(23.125060059288938),
            vr=int(71),
            rssi=float(9.248979369730092)
        )
        return instance

    
    def test_icao24_property(self):
        """
        Test icao24 property
        """
        test_value = 'ddsovwhourmbuqnyyruv'
        self.instance.icao24 = test_value
        self.assertEqual(self.instance.icao24, test_value)
    
    def test_receiver_id_property(self):
        """
        Test receiver_id property
        """
        test_value = 'rbcvzbyhryxufbnanpfo'
        self.instance.receiver_id = test_value
        self.assertEqual(self.instance.receiver_id, test_value)
    
    def test_msg_type_property(self):
        """
        Test msg_type property
        """
        test_value = 'hlgwxujwwedhyozepnkr'
        self.instance.msg_type = test_value
        self.assertEqual(self.instance.msg_type, test_value)
    
    def test_ts_property(self):
        """
        Test ts property
        """
        test_value = int(74)
        self.instance.ts = test_value
        self.assertEqual(self.instance.ts, test_value)
    
    def test_df_property(self):
        """
        Test df property
        """
        test_value = int(49)
        self.instance.df = test_value
        self.assertEqual(self.instance.df, test_value)
    
    def test_tc_property(self):
        """
        Test tc property
        """
        test_value = int(11)
        self.instance.tc = test_value
        self.assertEqual(self.instance.tc, test_value)
    
    def test_bcode_property(self):
        """
        Test bcode property
        """
        test_value = 'zjpalbxtscxsnnjetxyk'
        self.instance.bcode = test_value
        self.assertEqual(self.instance.bcode, test_value)
    
    def test_alt_property(self):
        """
        Test alt property
        """
        test_value = int(72)
        self.instance.alt = test_value
        self.assertEqual(self.instance.alt, test_value)
    
    def test_cs_property(self):
        """
        Test cs property
        """
        test_value = 'zmncsiyjwlmkvgahwnjv'
        self.instance.cs = test_value
        self.assertEqual(self.instance.cs, test_value)
    
    def test_sq_property(self):
        """
        Test sq property
        """
        test_value = 'gedgnyhywwbgbohaaeam'
        self.instance.sq = test_value
        self.assertEqual(self.instance.sq, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(70.76614598548544)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(58.267423003742216)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_spd_property(self):
        """
        Test spd property
        """
        test_value = float(11.856856640287516)
        self.instance.spd = test_value
        self.assertEqual(self.instance.spd, test_value)
    
    def test_ang_property(self):
        """
        Test ang property
        """
        test_value = float(23.125060059288938)
        self.instance.ang = test_value
        self.assertEqual(self.instance.ang, test_value)
    
    def test_vr_property(self):
        """
        Test vr property
        """
        test_value = int(71)
        self.instance.vr = test_value
        self.assertEqual(self.instance.vr, test_value)
    
    def test_rssi_property(self):
        """
        Test rssi property
        """
        test_value = float(9.248979369730092)
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

