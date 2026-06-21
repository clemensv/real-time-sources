"""
Test case for StationMetadata
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from erddap_producer_data.stationmetadata import StationMetadata


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
            erddap_id='pbnekclnmwdoittupxei',
            dataset_id='ggcjyfsciswanncdhoko',
            base_url='ojlckawtxygvlzepmooh',
            station_id='wqwyexoalcdgxjdzkudo',
            station_name='jmooilizqufdswerpbwi',
            station_id_variable='cyueleczvxqestgrwnrj',
            latitude=float(22.387931255165437),
            longitude=float(66.86740870429911),
            depth=float(98.44071758551969),
            attributes={'zdyzrewhzcrfoyctqrvd': 'xqypzxktclqlfajlxpnt'}
        )
        return instance

    
    def test_erddap_id_property(self):
        """
        Test erddap_id property
        """
        test_value = 'pbnekclnmwdoittupxei'
        self.instance.erddap_id = test_value
        self.assertEqual(self.instance.erddap_id, test_value)
    
    def test_dataset_id_property(self):
        """
        Test dataset_id property
        """
        test_value = 'ggcjyfsciswanncdhoko'
        self.instance.dataset_id = test_value
        self.assertEqual(self.instance.dataset_id, test_value)
    
    def test_base_url_property(self):
        """
        Test base_url property
        """
        test_value = 'ojlckawtxygvlzepmooh'
        self.instance.base_url = test_value
        self.assertEqual(self.instance.base_url, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'wqwyexoalcdgxjdzkudo'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'jmooilizqufdswerpbwi'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_station_id_variable_property(self):
        """
        Test station_id_variable property
        """
        test_value = 'cyueleczvxqestgrwnrj'
        self.instance.station_id_variable = test_value
        self.assertEqual(self.instance.station_id_variable, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(22.387931255165437)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(66.86740870429911)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_depth_property(self):
        """
        Test depth property
        """
        test_value = float(98.44071758551969)
        self.instance.depth = test_value
        self.assertEqual(self.instance.depth, test_value)
    
    def test_attributes_property(self):
        """
        Test attributes property
        """
        test_value = {'zdyzrewhzcrfoyctqrvd': 'xqypzxktclqlfajlxpnt'}
        self.instance.attributes = test_value
        self.assertEqual(self.instance.attributes, test_value)
    
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

