"""
Test case for SensorConfiguration
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wallonia_issep_producer_data.sensorconfiguration import SensorConfiguration


class Test_SensorConfiguration(unittest.TestCase):
    """
    Test case for SensorConfiguration
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SensorConfiguration.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SensorConfiguration for testing
        """
        instance = SensorConfiguration(
            configuration_id='vgqghiccoffedsmaxmfj'
        )
        return instance

    
    def test_configuration_id_property(self):
        """
        Test configuration_id property
        """
        test_value = 'vgqghiccoffedsmaxmfj'
        self.instance.configuration_id = test_value
        self.assertEqual(self.instance.configuration_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SensorConfiguration.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SensorConfiguration.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

