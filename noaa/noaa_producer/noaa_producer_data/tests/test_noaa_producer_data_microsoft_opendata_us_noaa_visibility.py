"""
Test case for Visibility
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_producer_data.microsoft.opendata.us.noaa.visibility import Visibility


class Test_Visibility(unittest.TestCase):
    """
    Test case for Visibility
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Visibility.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Visibility for testing
        """
        instance = Visibility(
            timestamp='karorgerblgeyznnxjrz',
            value=float(26.454340921361606),
            max_visibility_exceeded=False,
            min_visibility_exceeded=True,
            rate_of_change_exceeded=False,
            station_id='cktupstougnvuzkistzp'
        )
        return instance

    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'karorgerblgeyznnxjrz'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(26.454340921361606)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_max_visibility_exceeded_property(self):
        """
        Test max_visibility_exceeded property
        """
        test_value = False
        self.instance.max_visibility_exceeded = test_value
        self.assertEqual(self.instance.max_visibility_exceeded, test_value)
    
    def test_min_visibility_exceeded_property(self):
        """
        Test min_visibility_exceeded property
        """
        test_value = True
        self.instance.min_visibility_exceeded = test_value
        self.assertEqual(self.instance.min_visibility_exceeded, test_value)
    
    def test_rate_of_change_exceeded_property(self):
        """
        Test rate_of_change_exceeded property
        """
        test_value = False
        self.instance.rate_of_change_exceeded = test_value
        self.assertEqual(self.instance.rate_of_change_exceeded, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'cktupstougnvuzkistzp'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Visibility.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
