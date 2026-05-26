"""
Test case for StationMetadata
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_amqp_producer_data.stationmetadata import StationMetadata


class Test_StationMetadata(unittest.TestCase):
    """
    Test case for StationMetadata
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StationMetadata.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StationMetadata for testing
        """
        instance = StationMetadata(
            station_id='qrinsqgcrdiyoowkzkhr',
            station_name='qflplhtlhtickshbzlbn',
            latitude=float(42.05722051874745),
            longitude=float(61.946643050819716),
            elevation=float(4.83901553593774),
            state='tkdazmoavdcqbkdxqhrm',
            from_date='nkagrtirrnfbzsotbboe',
            to_date='wqeftlqfmoztygivwfoc'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'qrinsqgcrdiyoowkzkhr'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'qflplhtlhtickshbzlbn'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(42.05722051874745)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(61.946643050819716)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_elevation_property(self):
        """
        Test elevation property
        """
        test_value = float(4.83901553593774)
        self.instance.elevation = test_value
        self.assertEqual(self.instance.elevation, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'tkdazmoavdcqbkdxqhrm'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_from_date_property(self):
        """
        Test from_date property
        """
        test_value = 'nkagrtirrnfbzsotbboe'
        self.instance.from_date = test_value
        self.assertEqual(self.instance.from_date, test_value)
    
    def test_to_date_property(self):
        """
        Test to_date property
        """
        test_value = 'wqeftlqfmoztygivwfoc'
        self.instance.to_date = test_value
        self.assertEqual(self.instance.to_date, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StationMetadata.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StationMetadata.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

