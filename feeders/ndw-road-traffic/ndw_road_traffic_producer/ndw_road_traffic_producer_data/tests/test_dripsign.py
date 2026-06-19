"""
Test case for DripSign
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndw_road_traffic_producer_data.dripsign import DripSign


class Test_DripSign(unittest.TestCase):
    """
    Test case for DripSign
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DripSign.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DripSign for testing
        """
        instance = DripSign(
            vms_controller_id='apdjlkbyijlkgejfstyr',
            vms_index='wssjrrbbsvmwbqlikovc',
            vms_type='wrqeylkbwklammgukezm',
            latitude=float(7.811427190070763),
            longitude=float(55.24377304770908),
            road_name='gqkfwoxlxpjopnaulewo',
            description='ptmqtdgrkdfchzcsasil'
        )
        return instance

    
    def test_vms_controller_id_property(self):
        """
        Test vms_controller_id property
        """
        test_value = 'apdjlkbyijlkgejfstyr'
        self.instance.vms_controller_id = test_value
        self.assertEqual(self.instance.vms_controller_id, test_value)
    
    def test_vms_index_property(self):
        """
        Test vms_index property
        """
        test_value = 'wssjrrbbsvmwbqlikovc'
        self.instance.vms_index = test_value
        self.assertEqual(self.instance.vms_index, test_value)
    
    def test_vms_type_property(self):
        """
        Test vms_type property
        """
        test_value = 'wrqeylkbwklammgukezm'
        self.instance.vms_type = test_value
        self.assertEqual(self.instance.vms_type, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(7.811427190070763)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(55.24377304770908)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_road_name_property(self):
        """
        Test road_name property
        """
        test_value = 'gqkfwoxlxpjopnaulewo'
        self.instance.road_name = test_value
        self.assertEqual(self.instance.road_name, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'ptmqtdgrkdfchzcsasil'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DripSign.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DripSign.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

