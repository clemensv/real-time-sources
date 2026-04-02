"""
Test case for AirPressure
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_producer_data.microsoft.opendata.us.noaa.airpressure import AirPressure


class Test_AirPressure(unittest.TestCase):
    """
    Test case for AirPressure
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AirPressure.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AirPressure for testing
        """
        instance = AirPressure(
            station_id='vtbihwuysbcbrmmwofru',
            timestamp='onduvbtcjiczidwqxvfp',
            value=float(11.342214306903898),
            max_pressure_exceeded=True,
            min_pressure_exceeded=False,
            rate_of_change_exceeded=False
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'vtbihwuysbcbrmmwofru'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'onduvbtcjiczidwqxvfp'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(11.342214306903898)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_max_pressure_exceeded_property(self):
        """
        Test max_pressure_exceeded property
        """
        test_value = True
        self.instance.max_pressure_exceeded = test_value
        self.assertEqual(self.instance.max_pressure_exceeded, test_value)
    
    def test_min_pressure_exceeded_property(self):
        """
        Test min_pressure_exceeded property
        """
        test_value = False
        self.instance.min_pressure_exceeded = test_value
        self.assertEqual(self.instance.min_pressure_exceeded, test_value)
    
    def test_rate_of_change_exceeded_property(self):
        """
        Test rate_of_change_exceeded property
        """
        test_value = False
        self.instance.rate_of_change_exceeded = test_value
        self.assertEqual(self.instance.rate_of_change_exceeded, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AirPressure.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
