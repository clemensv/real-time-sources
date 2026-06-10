"""
Test case for Conductivity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_mqtt_producer_data.microsoft.opendata.us.noaa.conductivity import Conductivity


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
            station_id='gchyzdzhcyozznpmzyvo',
            timestamp='cjyldodfzvbkfikpzzht',
            value=float(28.171126071363716),
            max_conductivity_exceeded=False,
            min_conductivity_exceeded=False,
            rate_of_change_exceeded=False,
            region='jjilcaohropumvdrqiqa'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'gchyzdzhcyozznpmzyvo'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'cjyldodfzvbkfikpzzht'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(28.171126071363716)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_max_conductivity_exceeded_property(self):
        """
        Test max_conductivity_exceeded property
        """
        test_value = False
        self.instance.max_conductivity_exceeded = test_value
        self.assertEqual(self.instance.max_conductivity_exceeded, test_value)
    
    def test_min_conductivity_exceeded_property(self):
        """
        Test min_conductivity_exceeded property
        """
        test_value = False
        self.instance.min_conductivity_exceeded = test_value
        self.assertEqual(self.instance.min_conductivity_exceeded, test_value)
    
    def test_rate_of_change_exceeded_property(self):
        """
        Test rate_of_change_exceeded property
        """
        test_value = False
        self.instance.rate_of_change_exceeded = test_value
        self.assertEqual(self.instance.rate_of_change_exceeded, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'jjilcaohropumvdrqiqa'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Conductivity.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Conductivity.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

