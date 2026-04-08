"""
Test case for Berth
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_producer_data.berth import Berth


class Test_Berth(unittest.TestCase):
    """
    Test case for Berth
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Berth.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Berth for testing
        """
        instance = Berth(
            port_area_code='vxzbqorwchyjwgxsbgpj',
            berth_code='ewawbkgseeafiteywixf',
            berth_name='jfcilklfsnvdntclgkoz'
        )
        return instance

    
    def test_port_area_code_property(self):
        """
        Test port_area_code property
        """
        test_value = 'vxzbqorwchyjwgxsbgpj'
        self.instance.port_area_code = test_value
        self.assertEqual(self.instance.port_area_code, test_value)
    
    def test_berth_code_property(self):
        """
        Test berth_code property
        """
        test_value = 'ewawbkgseeafiteywixf'
        self.instance.berth_code = test_value
        self.assertEqual(self.instance.berth_code, test_value)
    
    def test_berth_name_property(self):
        """
        Test berth_name property
        """
        test_value = 'jfcilklfsnvdntclgkoz'
        self.instance.berth_name = test_value
        self.assertEqual(self.instance.berth_name, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Berth.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Berth.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

