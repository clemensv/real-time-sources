"""
Test case for MountainPassCondition
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_amqp_producer_data.us.wa.wsdot.mountainpass.mountainpasscondition import MountainPassCondition


class Test_MountainPassCondition(unittest.TestCase):
    """
    Test case for MountainPassCondition
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MountainPassCondition.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MountainPassCondition for testing
        """
        instance = MountainPassCondition(
            mountain_pass_id='ibogcqsceeukqmmqagpj',
            mountain_pass_name='ofnjnatpffzjcxubhieh',
            elevation_in_feet=int(71),
            latitude=float(12.71568590969604),
            longitude=float(76.9350105615753),
            temperature_in_fahrenheit=int(11),
            weather_condition='ruknfxlenlrwnxyojorg',
            road_condition='shxaoitfejewvdmmtqcp',
            travel_advisory_active=True,
            restriction_one_direction='ybfyldiktucpdpdyomby',
            restriction_one_text='kchzxzcotokppomnatzk',
            restriction_two_direction='fzxbzwgoegmabssfxbnl',
            restriction_two_text='ugrgygbdqtzoavmkocaf',
            date_updated='iavrzpsxhuoaxalwswnn'
        )
        return instance

    
    def test_mountain_pass_id_property(self):
        """
        Test mountain_pass_id property
        """
        test_value = 'ibogcqsceeukqmmqagpj'
        self.instance.mountain_pass_id = test_value
        self.assertEqual(self.instance.mountain_pass_id, test_value)
    
    def test_mountain_pass_name_property(self):
        """
        Test mountain_pass_name property
        """
        test_value = 'ofnjnatpffzjcxubhieh'
        self.instance.mountain_pass_name = test_value
        self.assertEqual(self.instance.mountain_pass_name, test_value)
    
    def test_elevation_in_feet_property(self):
        """
        Test elevation_in_feet property
        """
        test_value = int(71)
        self.instance.elevation_in_feet = test_value
        self.assertEqual(self.instance.elevation_in_feet, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(12.71568590969604)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(76.9350105615753)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_temperature_in_fahrenheit_property(self):
        """
        Test temperature_in_fahrenheit property
        """
        test_value = int(11)
        self.instance.temperature_in_fahrenheit = test_value
        self.assertEqual(self.instance.temperature_in_fahrenheit, test_value)
    
    def test_weather_condition_property(self):
        """
        Test weather_condition property
        """
        test_value = 'ruknfxlenlrwnxyojorg'
        self.instance.weather_condition = test_value
        self.assertEqual(self.instance.weather_condition, test_value)
    
    def test_road_condition_property(self):
        """
        Test road_condition property
        """
        test_value = 'shxaoitfejewvdmmtqcp'
        self.instance.road_condition = test_value
        self.assertEqual(self.instance.road_condition, test_value)
    
    def test_travel_advisory_active_property(self):
        """
        Test travel_advisory_active property
        """
        test_value = True
        self.instance.travel_advisory_active = test_value
        self.assertEqual(self.instance.travel_advisory_active, test_value)
    
    def test_restriction_one_direction_property(self):
        """
        Test restriction_one_direction property
        """
        test_value = 'ybfyldiktucpdpdyomby'
        self.instance.restriction_one_direction = test_value
        self.assertEqual(self.instance.restriction_one_direction, test_value)
    
    def test_restriction_one_text_property(self):
        """
        Test restriction_one_text property
        """
        test_value = 'kchzxzcotokppomnatzk'
        self.instance.restriction_one_text = test_value
        self.assertEqual(self.instance.restriction_one_text, test_value)
    
    def test_restriction_two_direction_property(self):
        """
        Test restriction_two_direction property
        """
        test_value = 'fzxbzwgoegmabssfxbnl'
        self.instance.restriction_two_direction = test_value
        self.assertEqual(self.instance.restriction_two_direction, test_value)
    
    def test_restriction_two_text_property(self):
        """
        Test restriction_two_text property
        """
        test_value = 'ugrgygbdqtzoavmkocaf'
        self.instance.restriction_two_text = test_value
        self.assertEqual(self.instance.restriction_two_text, test_value)
    
    def test_date_updated_property(self):
        """
        Test date_updated property
        """
        test_value = 'iavrzpsxhuoaxalwswnn'
        self.instance.date_updated = test_value
        self.assertEqual(self.instance.date_updated, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MountainPassCondition.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MountainPassCondition.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

