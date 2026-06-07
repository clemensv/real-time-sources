"""
Test case for AffectedCity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_quake_producer_data.affectedcity import AffectedCity
from jma_bosai_quake_producer_data.maxintensityenum import MaxIntensityenum


class Test_AffectedCity(unittest.TestCase):
    """
    Test case for AffectedCity
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AffectedCity.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AffectedCity for testing
        """
        instance = AffectedCity(
            prefecture_code='xpwjzqucnecluettowqw',
            city_code='ltkmrmufxcnmaxkivwsn',
            max_intensity=MaxIntensityenum.INTENSITY_1
        )
        return instance

    
    def test_prefecture_code_property(self):
        """
        Test prefecture_code property
        """
        test_value = 'xpwjzqucnecluettowqw'
        self.instance.prefecture_code = test_value
        self.assertEqual(self.instance.prefecture_code, test_value)
    
    def test_city_code_property(self):
        """
        Test city_code property
        """
        test_value = 'ltkmrmufxcnmaxkivwsn'
        self.instance.city_code = test_value
        self.assertEqual(self.instance.city_code, test_value)
    
    def test_max_intensity_property(self):
        """
        Test max_intensity property
        """
        test_value = MaxIntensityenum.INTENSITY_1
        self.instance.max_intensity = test_value
        self.assertEqual(self.instance.max_intensity, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AffectedCity.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = AffectedCity.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)


