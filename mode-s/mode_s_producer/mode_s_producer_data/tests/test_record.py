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
            icao24='nmctpxkvpvjlgacggyoe',
            receiver_id='eakqqgmeowmepxfsnzzi',
            msg_type='lmjtkutmblpvplfwhjzr',
            ts=int(3),
            df=int(22),
            tc=int(16),
            bcode='cvrqccvipfekqertedby',
            alt=int(40),
            cs='wspnivlufkoiskrywzqy',
            sq='cdurlcewyyiypstuvagi',
            lat=float(71.91754031762038),
            lon=float(67.32187138487407),
            spd=float(78.72226491247224),
            ang=float(84.53843833127611),
            vr=int(60),
            rssi=float(33.61495405371511)
        )
        return instance

    
    def test_icao24_property(self):
        """
        Test icao24 property
        """
        test_value = 'nmctpxkvpvjlgacggyoe'
        self.instance.icao24 = test_value
        self.assertEqual(self.instance.icao24, test_value)
    
    def test_receiver_id_property(self):
        """
        Test receiver_id property
        """
        test_value = 'eakqqgmeowmepxfsnzzi'
        self.instance.receiver_id = test_value
        self.assertEqual(self.instance.receiver_id, test_value)
    
    def test_msg_type_property(self):
        """
        Test msg_type property
        """
        test_value = 'lmjtkutmblpvplfwhjzr'
        self.instance.msg_type = test_value
        self.assertEqual(self.instance.msg_type, test_value)
    
    def test_ts_property(self):
        """
        Test ts property
        """
        test_value = int(3)
        self.instance.ts = test_value
        self.assertEqual(self.instance.ts, test_value)
    
    def test_df_property(self):
        """
        Test df property
        """
        test_value = int(22)
        self.instance.df = test_value
        self.assertEqual(self.instance.df, test_value)
    
    def test_tc_property(self):
        """
        Test tc property
        """
        test_value = int(16)
        self.instance.tc = test_value
        self.assertEqual(self.instance.tc, test_value)
    
    def test_bcode_property(self):
        """
        Test bcode property
        """
        test_value = 'cvrqccvipfekqertedby'
        self.instance.bcode = test_value
        self.assertEqual(self.instance.bcode, test_value)
    
    def test_alt_property(self):
        """
        Test alt property
        """
        test_value = int(40)
        self.instance.alt = test_value
        self.assertEqual(self.instance.alt, test_value)
    
    def test_cs_property(self):
        """
        Test cs property
        """
        test_value = 'wspnivlufkoiskrywzqy'
        self.instance.cs = test_value
        self.assertEqual(self.instance.cs, test_value)
    
    def test_sq_property(self):
        """
        Test sq property
        """
        test_value = 'cdurlcewyyiypstuvagi'
        self.instance.sq = test_value
        self.assertEqual(self.instance.sq, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(71.91754031762038)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(67.32187138487407)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_spd_property(self):
        """
        Test spd property
        """
        test_value = float(78.72226491247224)
        self.instance.spd = test_value
        self.assertEqual(self.instance.spd, test_value)
    
    def test_ang_property(self):
        """
        Test ang property
        """
        test_value = float(84.53843833127611)
        self.instance.ang = test_value
        self.assertEqual(self.instance.ang, test_value)
    
    def test_vr_property(self):
        """
        Test vr property
        """
        test_value = int(60)
        self.instance.vr = test_value
        self.assertEqual(self.instance.vr, test_value)
    
    def test_rssi_property(self):
        """
        Test rssi property
        """
        test_value = float(33.61495405371511)
        self.instance.rssi = test_value
        self.assertEqual(self.instance.rssi, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Record.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
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

