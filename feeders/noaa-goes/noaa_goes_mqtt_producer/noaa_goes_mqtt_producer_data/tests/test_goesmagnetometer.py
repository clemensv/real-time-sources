"""
Test case for GoesMagnetometer
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_goes_mqtt_producer_data.goesmagnetometer import GoesMagnetometer


class Test_GoesMagnetometer(unittest.TestCase):
    """
    Test case for GoesMagnetometer
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_GoesMagnetometer.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of GoesMagnetometer for testing
        """
        instance = GoesMagnetometer(
            time_tag='mepgcnhncvshjjgwqyco',
            satellite=int(94),
            he=float(59.41507646250641),
            hp=float(60.876094376702326),
            hn=float(44.43215682751526),
            total=float(17.90704875327024),
            arcjet_flag=True
        )
        return instance

    
    def test_time_tag_property(self):
        """
        Test time_tag property
        """
        test_value = 'mepgcnhncvshjjgwqyco'
        self.instance.time_tag = test_value
        self.assertEqual(self.instance.time_tag, test_value)
    
    def test_satellite_property(self):
        """
        Test satellite property
        """
        test_value = int(94)
        self.instance.satellite = test_value
        self.assertEqual(self.instance.satellite, test_value)
    
    def test_he_property(self):
        """
        Test he property
        """
        test_value = float(59.41507646250641)
        self.instance.he = test_value
        self.assertEqual(self.instance.he, test_value)
    
    def test_hp_property(self):
        """
        Test hp property
        """
        test_value = float(60.876094376702326)
        self.instance.hp = test_value
        self.assertEqual(self.instance.hp, test_value)
    
    def test_hn_property(self):
        """
        Test hn property
        """
        test_value = float(44.43215682751526)
        self.instance.hn = test_value
        self.assertEqual(self.instance.hn, test_value)
    
    def test_total_property(self):
        """
        Test total property
        """
        test_value = float(17.90704875327024)
        self.instance.total = test_value
        self.assertEqual(self.instance.total, test_value)
    
    def test_arcjet_flag_property(self):
        """
        Test arcjet_flag property
        """
        test_value = True
        self.instance.arcjet_flag = test_value
        self.assertEqual(self.instance.arcjet_flag, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = GoesMagnetometer.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = GoesMagnetometer.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

