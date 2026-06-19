"""
Test case for StationInformation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gbfs_bikeshare_amqp_producer_data.stationinformation import StationInformation


class Test_StationInformation(unittest.TestCase):
    """
    Test case for StationInformation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StationInformation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StationInformation for testing
        """
        instance = StationInformation(
            system_id='nnlexwranlpwfbsksaqb',
            station_id='zgdcbbtmvtozbthobzzi',
            name='xpautmoptafqhgcgvjze',
            short_name='jduntdxcdklxpvdhmasi',
            lat=float(44.66228898833246),
            lon=float(29.226435227383508),
            capacity=int(85),
            region_id='adldooeuhucaunlrjnkj',
            address='zpkzlkxbakcbmsvcclir',
            post_code='trmdbdrxuvewivxgnpcu'
        )
        return instance

    
    def test_system_id_property(self):
        """
        Test system_id property
        """
        test_value = 'nnlexwranlpwfbsksaqb'
        self.instance.system_id = test_value
        self.assertEqual(self.instance.system_id, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'zgdcbbtmvtozbthobzzi'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'xpautmoptafqhgcgvjze'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_short_name_property(self):
        """
        Test short_name property
        """
        test_value = 'jduntdxcdklxpvdhmasi'
        self.instance.short_name = test_value
        self.assertEqual(self.instance.short_name, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(44.66228898833246)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(29.226435227383508)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_capacity_property(self):
        """
        Test capacity property
        """
        test_value = int(85)
        self.instance.capacity = test_value
        self.assertEqual(self.instance.capacity, test_value)
    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = 'adldooeuhucaunlrjnkj'
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_address_property(self):
        """
        Test address property
        """
        test_value = 'zpkzlkxbakcbmsvcclir'
        self.instance.address = test_value
        self.assertEqual(self.instance.address, test_value)
    
    def test_post_code_property(self):
        """
        Test post_code property
        """
        test_value = 'trmdbdrxuvewivxgnpcu'
        self.instance.post_code = test_value
        self.assertEqual(self.instance.post_code, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StationInformation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StationInformation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

