"""
Test case for Conductivity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_producer_data.microsoft.opendata.us.noaa.conductivity import Conductivity


class Test_Conductivity(unittest.TestCase):
    """
    Test case for Conductivity
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Conductivity.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Conductivity for testing
        """
        instance = Conductivity(
            station_id='rpplzhvoypslqxzozjny',
            timestamp='wjtwypmaffepgiyuicrv',
            value=float(40.33585096410079),
            max_conductivity_exceeded=True,
            min_conductivity_exceeded=True,
            rate_of_change_exceeded=False
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'rpplzhvoypslqxzozjny'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'wjtwypmaffepgiyuicrv'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(40.33585096410079)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_max_conductivity_exceeded_property(self):
        """
        Test max_conductivity_exceeded property
        """
        test_value = True
        self.instance.max_conductivity_exceeded = test_value
        self.assertEqual(self.instance.max_conductivity_exceeded, test_value)
    
    def test_min_conductivity_exceeded_property(self):
        """
        Test min_conductivity_exceeded property
        """
        test_value = True
        self.instance.min_conductivity_exceeded = test_value
        self.assertEqual(self.instance.min_conductivity_exceeded, test_value)
    
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
        new_instance = Conductivity.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
