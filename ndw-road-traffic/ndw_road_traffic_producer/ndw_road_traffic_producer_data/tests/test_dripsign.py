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
            vms_controller_id='bpwcwemlhaqkpdprbkqc',
            vms_index='vhxrczbcbqxtidtjaqbw',
            vms_type='eovgoqdgjrzxltbhyodh',
            latitude=float(45.51964463592029),
            longitude=float(89.12610520982433),
            road_name='dovjsiikxdeygudspkwr',
            description='ibjlzkwneknozaclijat'
        )
        return instance

    
    def test_vms_controller_id_property(self):
        """
        Test vms_controller_id property
        """
        test_value = 'bpwcwemlhaqkpdprbkqc'
        self.instance.vms_controller_id = test_value
        self.assertEqual(self.instance.vms_controller_id, test_value)
    
    def test_vms_index_property(self):
        """
        Test vms_index property
        """
        test_value = 'vhxrczbcbqxtidtjaqbw'
        self.instance.vms_index = test_value
        self.assertEqual(self.instance.vms_index, test_value)
    
    def test_vms_type_property(self):
        """
        Test vms_type property
        """
        test_value = 'eovgoqdgjrzxltbhyodh'
        self.instance.vms_type = test_value
        self.assertEqual(self.instance.vms_type, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(45.51964463592029)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(89.12610520982433)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_road_name_property(self):
        """
        Test road_name property
        """
        test_value = 'dovjsiikxdeygudspkwr'
        self.instance.road_name = test_value
        self.assertEqual(self.instance.road_name, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'ibjlzkwneknozaclijat'
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

