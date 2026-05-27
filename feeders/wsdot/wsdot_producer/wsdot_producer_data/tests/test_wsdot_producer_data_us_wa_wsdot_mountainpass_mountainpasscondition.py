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
            mountain_pass_id='xikzhqoychamcyokltuf',
            mountain_pass_name='yjhbzuhzniaaqshavfvh',
            elevation_in_feet=int(1),
            latitude=float(92.1363500820559),
            longitude=float(58.66194618724339),
            temperature_in_fahrenheit=int(64),
            weather_condition='tsytdsrshgeaantfqsxt',
            road_condition='daceomnfdsjqxkpgujnl',
            travel_advisory_active=True,
            restriction_one_direction='wvfhgwtizxljbblcmqzp',
            restriction_one_text='ztgoduuqbllzcdzafcta',
            restriction_two_direction='eavdvlicmurysajuhghg',
            restriction_two_text='fevzffygutaegdvlwdyx',
            date_updated='jgaljzuhpfkauqxclmua'
        )
        return instance

    
    def test_mountain_pass_id_property(self):
        """
        Test mountain_pass_id property
        """
        test_value = 'xikzhqoychamcyokltuf'
        self.instance.mountain_pass_id = test_value
        self.assertEqual(self.instance.mountain_pass_id, test_value)
    
    def test_mountain_pass_name_property(self):
        """
        Test mountain_pass_name property
        """
        test_value = 'yjhbzuhzniaaqshavfvh'
        self.instance.mountain_pass_name = test_value
        self.assertEqual(self.instance.mountain_pass_name, test_value)
    
    def test_elevation_in_feet_property(self):
        """
        Test elevation_in_feet property
        """
        test_value = int(1)
        self.instance.elevation_in_feet = test_value
        self.assertEqual(self.instance.elevation_in_feet, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(92.1363500820559)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(58.66194618724339)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_temperature_in_fahrenheit_property(self):
        """
        Test temperature_in_fahrenheit property
        """
        test_value = int(64)
        self.instance.temperature_in_fahrenheit = test_value
        self.assertEqual(self.instance.temperature_in_fahrenheit, test_value)
    
    def test_weather_condition_property(self):
        """
        Test weather_condition property
        """
        test_value = 'tsytdsrshgeaantfqsxt'
        self.instance.weather_condition = test_value
        self.assertEqual(self.instance.weather_condition, test_value)
    
    def test_road_condition_property(self):
        """
        Test road_condition property
        """
        test_value = 'daceomnfdsjqxkpgujnl'
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
        test_value = 'wvfhgwtizxljbblcmqzp'
        self.instance.restriction_one_direction = test_value
        self.assertEqual(self.instance.restriction_one_direction, test_value)
    
    def test_restriction_one_text_property(self):
        """
        Test restriction_one_text property
        """
        test_value = 'ztgoduuqbllzcdzafcta'
        self.instance.restriction_one_text = test_value
        self.assertEqual(self.instance.restriction_one_text, test_value)
    
    def test_restriction_two_direction_property(self):
        """
        Test restriction_two_direction property
        """
        test_value = 'eavdvlicmurysajuhghg'
        self.instance.restriction_two_direction = test_value
        self.assertEqual(self.instance.restriction_two_direction, test_value)
    
    def test_restriction_two_text_property(self):
        """
        Test restriction_two_text property
        """
        test_value = 'fevzffygutaegdvlwdyx'
        self.instance.restriction_two_text = test_value
        self.assertEqual(self.instance.restriction_two_text, test_value)
    
    def test_date_updated_property(self):
        """
        Test date_updated property
        """
        test_value = 'jgaljzuhpfkauqxclmua'
        self.instance.date_updated = test_value
        self.assertEqual(self.instance.date_updated, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MountainPassCondition.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
