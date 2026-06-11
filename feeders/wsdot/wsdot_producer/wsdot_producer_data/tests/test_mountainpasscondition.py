"""
Test case for MountainPassCondition
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_producer_data.us.wa.wsdot.mountainpass.mountainpasscondition import MountainPassCondition


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
            mountain_pass_id='aqpxelherupvdrjqkjxs',
            mountain_pass_name='ygvlashfztqeaodewwtr',
            elevation_in_feet=int(44),
            latitude=float(16.914628491381865),
            longitude=float(99.53786230438001),
            temperature_in_fahrenheit=int(55),
            weather_condition='lmzxqajxooqicslmeyjv',
            road_condition='bypsjmlbavpqyhvkgjbn',
            travel_advisory_active=False,
            restriction_one_direction='ctohlutptvflwsncjuca',
            restriction_one_text='ivrjdqnguywdxlfzdffy',
            restriction_two_direction='qjsmacpbwjtzbpfzpsqp',
            restriction_two_text='lchwupzlnlheubxiibjg',
            date_updated='xgyagcnonbdhmbszgqpf'
        )
        return instance

    
    def test_mountain_pass_id_property(self):
        """
        Test mountain_pass_id property
        """
        test_value = 'aqpxelherupvdrjqkjxs'
        self.instance.mountain_pass_id = test_value
        self.assertEqual(self.instance.mountain_pass_id, test_value)
    
    def test_mountain_pass_name_property(self):
        """
        Test mountain_pass_name property
        """
        test_value = 'ygvlashfztqeaodewwtr'
        self.instance.mountain_pass_name = test_value
        self.assertEqual(self.instance.mountain_pass_name, test_value)
    
    def test_elevation_in_feet_property(self):
        """
        Test elevation_in_feet property
        """
        test_value = int(44)
        self.instance.elevation_in_feet = test_value
        self.assertEqual(self.instance.elevation_in_feet, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(16.914628491381865)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(99.53786230438001)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_temperature_in_fahrenheit_property(self):
        """
        Test temperature_in_fahrenheit property
        """
        test_value = int(55)
        self.instance.temperature_in_fahrenheit = test_value
        self.assertEqual(self.instance.temperature_in_fahrenheit, test_value)
    
    def test_weather_condition_property(self):
        """
        Test weather_condition property
        """
        test_value = 'lmzxqajxooqicslmeyjv'
        self.instance.weather_condition = test_value
        self.assertEqual(self.instance.weather_condition, test_value)
    
    def test_road_condition_property(self):
        """
        Test road_condition property
        """
        test_value = 'bypsjmlbavpqyhvkgjbn'
        self.instance.road_condition = test_value
        self.assertEqual(self.instance.road_condition, test_value)
    
    def test_travel_advisory_active_property(self):
        """
        Test travel_advisory_active property
        """
        test_value = False
        self.instance.travel_advisory_active = test_value
        self.assertEqual(self.instance.travel_advisory_active, test_value)
    
    def test_restriction_one_direction_property(self):
        """
        Test restriction_one_direction property
        """
        test_value = 'ctohlutptvflwsncjuca'
        self.instance.restriction_one_direction = test_value
        self.assertEqual(self.instance.restriction_one_direction, test_value)
    
    def test_restriction_one_text_property(self):
        """
        Test restriction_one_text property
        """
        test_value = 'ivrjdqnguywdxlfzdffy'
        self.instance.restriction_one_text = test_value
        self.assertEqual(self.instance.restriction_one_text, test_value)
    
    def test_restriction_two_direction_property(self):
        """
        Test restriction_two_direction property
        """
        test_value = 'qjsmacpbwjtzbpfzpsqp'
        self.instance.restriction_two_direction = test_value
        self.assertEqual(self.instance.restriction_two_direction, test_value)
    
    def test_restriction_two_text_property(self):
        """
        Test restriction_two_text property
        """
        test_value = 'lchwupzlnlheubxiibjg'
        self.instance.restriction_two_text = test_value
        self.assertEqual(self.instance.restriction_two_text, test_value)
    
    def test_date_updated_property(self):
        """
        Test date_updated property
        """
        test_value = 'xgyagcnonbdhmbszgqpf'
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

