"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hongkong_epd_producer_data.station import Station


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
            station_id='oaqpdqsrohplugxingrc',
            station_name='oljwwwwryxhdcvbsusvl',
            station_type='lcngdzpojruxfzwzdatx',
            district='yvwpxrrgooofvggwosfq',
            latitude=float(40.17040816010454),
            longitude=float(96.29498192472037)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'oaqpdqsrohplugxingrc'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'oljwwwwryxhdcvbsusvl'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = 'lcngdzpojruxfzwzdatx'
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_district_property(self):
        """
        Test district property
        """
        test_value = 'yvwpxrrgooofvggwosfq'
        self.instance.district = test_value
        self.assertEqual(self.instance.district, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(40.17040816010454)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(96.29498192472037)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Station.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

