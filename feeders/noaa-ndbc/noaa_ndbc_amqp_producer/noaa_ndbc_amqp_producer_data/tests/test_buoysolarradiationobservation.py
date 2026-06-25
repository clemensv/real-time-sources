"""
Test case for BuoySolarRadiationObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_amqp_producer_data.buoysolarradiationobservation import BuoySolarRadiationObservation
import datetime


class Test_BuoySolarRadiationObservation(unittest.TestCase):
    """
    Test case for BuoySolarRadiationObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BuoySolarRadiationObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BuoySolarRadiationObservation for testing
        """
        instance = BuoySolarRadiationObservation(
            station_id='qntoijwwsnbwmalyzees',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            shortwave_radiation_licor=float(85.7153747744605),
            shortwave_radiation_eppley=float(27.339324243591513),
            longwave_radiation=float(5.014127072305219),
            region='yzliuupdobqexhzcadmg'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'qntoijwwsnbwmalyzees'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_shortwave_radiation_licor_property(self):
        """
        Test shortwave_radiation_licor property
        """
        test_value = float(85.7153747744605)
        self.instance.shortwave_radiation_licor = test_value
        self.assertEqual(self.instance.shortwave_radiation_licor, test_value)
    
    def test_shortwave_radiation_eppley_property(self):
        """
        Test shortwave_radiation_eppley property
        """
        test_value = float(27.339324243591513)
        self.instance.shortwave_radiation_eppley = test_value
        self.assertEqual(self.instance.shortwave_radiation_eppley, test_value)
    
    def test_longwave_radiation_property(self):
        """
        Test longwave_radiation property
        """
        test_value = float(5.014127072305219)
        self.instance.longwave_radiation = test_value
        self.assertEqual(self.instance.longwave_radiation, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'yzliuupdobqexhzcadmg'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoySolarRadiationObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BuoySolarRadiationObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

