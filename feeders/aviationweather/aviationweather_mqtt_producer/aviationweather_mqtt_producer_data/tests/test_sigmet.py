"""
Test case for Sigmet
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aviationweather_mqtt_producer_data.sigmet import Sigmet
import datetime


class Test_Sigmet(unittest.TestCase):
    """
    Test case for Sigmet
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Sigmet.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Sigmet for testing
        """
        instance = Sigmet(
            icao_id='ykjqylwxsysvbatjbgna',
            series_id='mpausfvvdnkrvdoxipui',
            valid_time_from=datetime.datetime.now(datetime.timezone.utc),
            valid_time_to=datetime.datetime.now(datetime.timezone.utc),
            hazard='jyhyfgphhkqtdhaidqhw',
            qualifier='wmqfgmutagsyplkzikyf',
            sigmet_type='fvjidjzievnbkvxzxria',
            altitude_hi=int(29),
            altitude_low=int(59),
            movement_dir='cmevuoubfmeaimrnmenp',
            movement_spd='yfedsssgysoebltxgstx',
            severity='dnaysomjlljdhbowfaay',
            raw_sigmet='hpudgsjvlrfvdsnhhpja',
            coords='knzzqxihhbypmhmzfuxv',
            sigmet_id='fqpnghndmljjoyieheqc',
            region='uzgockyxrzntsoawzouh'
        )
        return instance

    
    def test_icao_id_property(self):
        """
        Test icao_id property
        """
        test_value = 'ykjqylwxsysvbatjbgna'
        self.instance.icao_id = test_value
        self.assertEqual(self.instance.icao_id, test_value)
    
    def test_series_id_property(self):
        """
        Test series_id property
        """
        test_value = 'mpausfvvdnkrvdoxipui'
        self.instance.series_id = test_value
        self.assertEqual(self.instance.series_id, test_value)
    
    def test_valid_time_from_property(self):
        """
        Test valid_time_from property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.valid_time_from = test_value
        self.assertEqual(self.instance.valid_time_from, test_value)
    
    def test_valid_time_to_property(self):
        """
        Test valid_time_to property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.valid_time_to = test_value
        self.assertEqual(self.instance.valid_time_to, test_value)
    
    def test_hazard_property(self):
        """
        Test hazard property
        """
        test_value = 'jyhyfgphhkqtdhaidqhw'
        self.instance.hazard = test_value
        self.assertEqual(self.instance.hazard, test_value)
    
    def test_qualifier_property(self):
        """
        Test qualifier property
        """
        test_value = 'wmqfgmutagsyplkzikyf'
        self.instance.qualifier = test_value
        self.assertEqual(self.instance.qualifier, test_value)
    
    def test_sigmet_type_property(self):
        """
        Test sigmet_type property
        """
        test_value = 'fvjidjzievnbkvxzxria'
        self.instance.sigmet_type = test_value
        self.assertEqual(self.instance.sigmet_type, test_value)
    
    def test_altitude_hi_property(self):
        """
        Test altitude_hi property
        """
        test_value = int(29)
        self.instance.altitude_hi = test_value
        self.assertEqual(self.instance.altitude_hi, test_value)
    
    def test_altitude_low_property(self):
        """
        Test altitude_low property
        """
        test_value = int(59)
        self.instance.altitude_low = test_value
        self.assertEqual(self.instance.altitude_low, test_value)
    
    def test_movement_dir_property(self):
        """
        Test movement_dir property
        """
        test_value = 'cmevuoubfmeaimrnmenp'
        self.instance.movement_dir = test_value
        self.assertEqual(self.instance.movement_dir, test_value)
    
    def test_movement_spd_property(self):
        """
        Test movement_spd property
        """
        test_value = 'yfedsssgysoebltxgstx'
        self.instance.movement_spd = test_value
        self.assertEqual(self.instance.movement_spd, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = 'dnaysomjlljdhbowfaay'
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_raw_sigmet_property(self):
        """
        Test raw_sigmet property
        """
        test_value = 'hpudgsjvlrfvdsnhhpja'
        self.instance.raw_sigmet = test_value
        self.assertEqual(self.instance.raw_sigmet, test_value)
    
    def test_coords_property(self):
        """
        Test coords property
        """
        test_value = 'knzzqxihhbypmhmzfuxv'
        self.instance.coords = test_value
        self.assertEqual(self.instance.coords, test_value)
    
    def test_sigmet_id_property(self):
        """
        Test sigmet_id property
        """
        test_value = 'fqpnghndmljjoyieheqc'
        self.instance.sigmet_id = test_value
        self.assertEqual(self.instance.sigmet_id, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'uzgockyxrzntsoawzouh'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Sigmet.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Sigmet.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

