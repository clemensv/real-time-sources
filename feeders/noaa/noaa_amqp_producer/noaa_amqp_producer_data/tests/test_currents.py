"""
Test case for Currents
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_amqp_producer_data.microsoft.opendata.us.noaa.currents import Currents


class Test_Currents(unittest.TestCase):
    """
    Test case for Currents
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Currents.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Currents for testing
        """
        instance = Currents(
            station_id='azngmhwkqoyjsppknaiu',
            timestamp='eaoniwandyawzavibmml',
            speed=float(32.28205761289126),
            direction_degrees=float(8.661804967973696),
            bin='thrulivroclvgkbiqayn',
            region='ydefuwakdhfcqkvihkxa'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'azngmhwkqoyjsppknaiu'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'eaoniwandyawzavibmml'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_speed_property(self):
        """
        Test speed property
        """
        test_value = float(32.28205761289126)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
    def test_direction_degrees_property(self):
        """
        Test direction_degrees property
        """
        test_value = float(8.661804967973696)
        self.instance.direction_degrees = test_value
        self.assertEqual(self.instance.direction_degrees, test_value)
    
    def test_bin_property(self):
        """
        Test bin property
        """
        test_value = 'thrulivroclvgkbiqayn'
        self.instance.bin = test_value
        self.assertEqual(self.instance.bin, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'ydefuwakdhfcqkvihkxa'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Currents.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Currents.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

