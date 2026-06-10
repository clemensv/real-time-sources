"""
Test case for GoesMagnetometer
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_goes_amqp_producer_data.goesmagnetometer import GoesMagnetometer


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
            time_tag='lwiqwwkixbruibegurjz',
            satellite=int(3),
            he=float(34.075591584629215),
            hp=float(59.78045199711711),
            hn=float(17.735412687018805),
            total=float(66.36415368869693),
            arcjet_flag=True
        )
        return instance

    
    def test_time_tag_property(self):
        """
        Test time_tag property
        """
        test_value = 'lwiqwwkixbruibegurjz'
        self.instance.time_tag = test_value
        self.assertEqual(self.instance.time_tag, test_value)
    
    def test_satellite_property(self):
        """
        Test satellite property
        """
        test_value = int(3)
        self.instance.satellite = test_value
        self.assertEqual(self.instance.satellite, test_value)
    
    def test_he_property(self):
        """
        Test he property
        """
        test_value = float(34.075591584629215)
        self.instance.he = test_value
        self.assertEqual(self.instance.he, test_value)
    
    def test_hp_property(self):
        """
        Test hp property
        """
        test_value = float(59.78045199711711)
        self.instance.hp = test_value
        self.assertEqual(self.instance.hp, test_value)
    
    def test_hn_property(self):
        """
        Test hn property
        """
        test_value = float(17.735412687018805)
        self.instance.hn = test_value
        self.assertEqual(self.instance.hn, test_value)
    
    def test_total_property(self):
        """
        Test total property
        """
        test_value = float(66.36415368869693)
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

