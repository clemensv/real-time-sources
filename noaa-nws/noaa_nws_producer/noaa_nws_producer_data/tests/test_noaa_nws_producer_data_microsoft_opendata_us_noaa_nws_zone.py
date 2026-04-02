"""
Test case for Zone
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_nws_producer_data.microsoft.opendata.us.noaa.nws.zone import Zone


class Test_Zone(unittest.TestCase):
    """
    Test case for Zone
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Zone.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Zone for testing
        """
        instance = Zone(
            zone_id='phbadrmumqnmzbykwzrs',
            name='hzdontqhczrttsyidbfl',
            type='uwbljobdxvqgfvhmubly',
            state='djgymqefdtcwtuqrfhkt',
            forecast_office='hzqndoaxrsgbualyvbya',
            timezone='fqparhwijqbtjxloaczf',
            radar_station='wqfmdhpqvtbhismvwvjz'
        )
        return instance

    
    def test_zone_id_property(self):
        """
        Test zone_id property
        """
        test_value = 'phbadrmumqnmzbykwzrs'
        self.instance.zone_id = test_value
        self.assertEqual(self.instance.zone_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'hzdontqhczrttsyidbfl'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'uwbljobdxvqgfvhmubly'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'djgymqefdtcwtuqrfhkt'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_forecast_office_property(self):
        """
        Test forecast_office property
        """
        test_value = 'hzqndoaxrsgbualyvbya'
        self.instance.forecast_office = test_value
        self.assertEqual(self.instance.forecast_office, test_value)
    
    def test_timezone_property(self):
        """
        Test timezone property
        """
        test_value = 'fqparhwijqbtjxloaczf'
        self.instance.timezone = test_value
        self.assertEqual(self.instance.timezone, test_value)
    
    def test_radar_station_property(self):
        """
        Test radar_station property
        """
        test_value = 'wqfmdhpqvtbhismvwvjz'
        self.instance.radar_station = test_value
        self.assertEqual(self.instance.radar_station, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Zone.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
