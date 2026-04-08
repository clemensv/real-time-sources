"""
Test case for BuoySolarRadiationObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_producer_data.microsoft.opendata.us.noaa.ndbc.buoysolarradiationobservation import BuoySolarRadiationObservation
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
            station_id='vnzgfrpetejymkrncmww',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            shortwave_radiation_licor=float(55.58353485772242),
            shortwave_radiation_eppley=float(45.783242103987355),
            longwave_radiation=float(27.50081193507986)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'vnzgfrpetejymkrncmww'
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
        test_value = float(55.58353485772242)
        self.instance.shortwave_radiation_licor = test_value
        self.assertEqual(self.instance.shortwave_radiation_licor, test_value)
    
    def test_shortwave_radiation_eppley_property(self):
        """
        Test shortwave_radiation_eppley property
        """
        test_value = float(45.783242103987355)
        self.instance.shortwave_radiation_eppley = test_value
        self.assertEqual(self.instance.shortwave_radiation_eppley, test_value)
    
    def test_longwave_radiation_property(self):
        """
        Test longwave_radiation property
        """
        test_value = float(27.50081193507986)
        self.instance.longwave_radiation = test_value
        self.assertEqual(self.instance.longwave_radiation, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoySolarRadiationObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
