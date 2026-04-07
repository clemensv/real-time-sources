"""
Test case for Wind
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_producer_data.microsoft.opendata.us.noaa.wind import Wind


class Test_Wind(unittest.TestCase):
    """
    Test case for Wind
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Wind.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Wind for testing
        """
        instance = Wind(
            station_id='otkohnowafdepxlwxrqz',
            timestamp='klqfdytmwncmfmdwxqgb',
            speed=float(73.63908107186165),
            direction_degrees='vfcuvnaauccwwqphnhms',
            direction_text='cqjqyrarwvcemgenjzim',
            gusts=float(62.02277903813954),
            max_wind_speed_exceeded=True,
            rate_of_change_exceeded=True
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'otkohnowafdepxlwxrqz'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'klqfdytmwncmfmdwxqgb'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_speed_property(self):
        """
        Test speed property
        """
        test_value = float(73.63908107186165)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
    def test_direction_degrees_property(self):
        """
        Test direction_degrees property
        """
        test_value = 'vfcuvnaauccwwqphnhms'
        self.instance.direction_degrees = test_value
        self.assertEqual(self.instance.direction_degrees, test_value)
    
    def test_direction_text_property(self):
        """
        Test direction_text property
        """
        test_value = 'cqjqyrarwvcemgenjzim'
        self.instance.direction_text = test_value
        self.assertEqual(self.instance.direction_text, test_value)
    
    def test_gusts_property(self):
        """
        Test gusts property
        """
        test_value = float(62.02277903813954)
        self.instance.gusts = test_value
        self.assertEqual(self.instance.gusts, test_value)
    
    def test_max_wind_speed_exceeded_property(self):
        """
        Test max_wind_speed_exceeded property
        """
        test_value = True
        self.instance.max_wind_speed_exceeded = test_value
        self.assertEqual(self.instance.max_wind_speed_exceeded, test_value)
    
    def test_rate_of_change_exceeded_property(self):
        """
        Test rate_of_change_exceeded property
        """
        test_value = True
        self.instance.rate_of_change_exceeded = test_value
        self.assertEqual(self.instance.rate_of_change_exceeded, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Wind.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
