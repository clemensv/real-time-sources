"""
Test case for AffectedPrefecture
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_quake_amqp_producer_data.affectedprefecture import AffectedPrefecture
from jma_bosai_quake_amqp_producer_data.maxintensityenum import MaxIntensityenum


class Test_AffectedPrefecture(unittest.TestCase):
    """
    Test case for AffectedPrefecture
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AffectedPrefecture.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AffectedPrefecture for testing
        """
        instance = AffectedPrefecture(
            code='wkqnheaasupmrjackjsd',
            max_intensity=MaxIntensityenum.VALUE_1
        )
        return instance

    
    def test_code_property(self):
        """
        Test code property
        """
        test_value = 'wkqnheaasupmrjackjsd'
        self.instance.code = test_value
        self.assertEqual(self.instance.code, test_value)
    
    def test_max_intensity_property(self):
        """
        Test max_intensity property
        """
        test_value = MaxIntensityenum.VALUE_1
        self.instance.max_intensity = test_value
        self.assertEqual(self.instance.max_intensity, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AffectedPrefecture.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = AffectedPrefecture.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

