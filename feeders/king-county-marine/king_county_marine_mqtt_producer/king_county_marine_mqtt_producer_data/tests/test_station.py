"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from king_county_marine_mqtt_producer_data.station import Station


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
            station_id='ejwbrnxkkydkhiiayogj',
            station_name='cmmgwjxghhbkmvmywhcv',
            dataset_id='iejyxebilqtyvsiwnxhh',
            dataset_name='wkesnzqwixpeeobatoel',
            dataset_url='grdlzemvsdmbkfduvxxt',
            sensor_level='urjxucepouvsqmnatpxr',
            latitude=float(61.91724474112619),
            longitude=float(47.390238055676384)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'ejwbrnxkkydkhiiayogj'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'cmmgwjxghhbkmvmywhcv'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_dataset_id_property(self):
        """
        Test dataset_id property
        """
        test_value = 'iejyxebilqtyvsiwnxhh'
        self.instance.dataset_id = test_value
        self.assertEqual(self.instance.dataset_id, test_value)
    
    def test_dataset_name_property(self):
        """
        Test dataset_name property
        """
        test_value = 'wkesnzqwixpeeobatoel'
        self.instance.dataset_name = test_value
        self.assertEqual(self.instance.dataset_name, test_value)
    
    def test_dataset_url_property(self):
        """
        Test dataset_url property
        """
        test_value = 'grdlzemvsdmbkfduvxxt'
        self.instance.dataset_url = test_value
        self.assertEqual(self.instance.dataset_url, test_value)
    
    def test_sensor_level_property(self):
        """
        Test sensor_level property
        """
        test_value = 'urjxucepouvsqmnatpxr'
        self.instance.sensor_level = test_value
        self.assertEqual(self.instance.sensor_level, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(61.91724474112619)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(47.390238055676384)
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

