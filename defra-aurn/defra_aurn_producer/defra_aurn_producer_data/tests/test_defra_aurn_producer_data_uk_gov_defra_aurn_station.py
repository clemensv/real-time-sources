"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from defra_aurn_producer_data.uk.gov.defra.aurn.station import Station


class Test_Station(unittest.TestCase):
    """
    Test case for Station
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Station.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Station for testing
        """
        instance = Station(
            station_id='kmgxhhxbfwtfpdllcgcd',
            label='dzqudbrgzafkgiuyeqfa',
            latitude=float(74.57841934569772),
            longitude=float(3.8113167502610845)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'kmgxhhxbfwtfpdllcgcd'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_label_property(self):
        """
        Test label property
        """
        test_value = 'dzqudbrgzafkgiuyeqfa'
        self.instance.label = test_value
        self.assertEqual(self.instance.label, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(74.57841934569772)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(3.8113167502610845)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
