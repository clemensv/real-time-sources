"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from king_county_marine_producer_data.station import Station


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
            station_id='ztbaakyyjdsaxedrzktb',
            station_name='biiexlycritghfsuvrgx',
            dataset_id='ypkydjedziympbzypzpb',
            dataset_name='wmiwquwtacioocjvpwsn',
            dataset_url='advqhsubqxcwklwidezk',
            sensor_level='rrzzcmgdioefiukzmpaf',
            latitude=float(47.319628562454305),
            longitude=float(88.84606888249795)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'ztbaakyyjdsaxedrzktb'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'biiexlycritghfsuvrgx'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_dataset_id_property(self):
        """
        Test dataset_id property
        """
        test_value = 'ypkydjedziympbzypzpb'
        self.instance.dataset_id = test_value
        self.assertEqual(self.instance.dataset_id, test_value)
    
    def test_dataset_name_property(self):
        """
        Test dataset_name property
        """
        test_value = 'wmiwquwtacioocjvpwsn'
        self.instance.dataset_name = test_value
        self.assertEqual(self.instance.dataset_name, test_value)
    
    def test_dataset_url_property(self):
        """
        Test dataset_url property
        """
        test_value = 'advqhsubqxcwklwidezk'
        self.instance.dataset_url = test_value
        self.assertEqual(self.instance.dataset_url, test_value)
    
    def test_sensor_level_property(self):
        """
        Test sensor_level property
        """
        test_value = 'rrzzcmgdioefiukzmpaf'
        self.instance.sensor_level = test_value
        self.assertEqual(self.instance.sensor_level, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(47.319628562454305)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(88.84606888249795)
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

