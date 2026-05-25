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
            mountain_pass_id='iqrlywcllqeirvyqdcrk',
            mountain_pass_name='ugmsgplugkkboknapqkz',
            elevation_in_feet=int(13),
            latitude=float(49.15246977843131),
            longitude=float(96.1329417377088),
            temperature_in_fahrenheit=int(46),
            weather_condition='btawqbqxsekzgfsfzcdj',
            road_condition='ztzajzncfrperjkezskg',
            travel_advisory_active=True,
            restriction_one_direction='ntekairzeffcokzhzity',
            restriction_one_text='tolpofedkwynzowvbunw',
            restriction_two_direction='euplfauqictbijlleqxo',
            restriction_two_text='oaxgrjtrsokrgzfocqvi',
            date_updated='nfaulagnjgtqxtiabtck'
        )
        return instance

    
    def test_mountain_pass_id_property(self):
        """
        Test mountain_pass_id property
        """
        test_value = 'iqrlywcllqeirvyqdcrk'
        self.instance.mountain_pass_id = test_value
        self.assertEqual(self.instance.mountain_pass_id, test_value)
    
    def test_mountain_pass_name_property(self):
        """
        Test mountain_pass_name property
        """
        test_value = 'ugmsgplugkkboknapqkz'
        self.instance.mountain_pass_name = test_value
        self.assertEqual(self.instance.mountain_pass_name, test_value)
    
    def test_elevation_in_feet_property(self):
        """
        Test elevation_in_feet property
        """
        test_value = int(13)
        self.instance.elevation_in_feet = test_value
        self.assertEqual(self.instance.elevation_in_feet, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(49.15246977843131)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(96.1329417377088)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_temperature_in_fahrenheit_property(self):
        """
        Test temperature_in_fahrenheit property
        """
        test_value = int(46)
        self.instance.temperature_in_fahrenheit = test_value
        self.assertEqual(self.instance.temperature_in_fahrenheit, test_value)
    
    def test_weather_condition_property(self):
        """
        Test weather_condition property
        """
        test_value = 'btawqbqxsekzgfsfzcdj'
        self.instance.weather_condition = test_value
        self.assertEqual(self.instance.weather_condition, test_value)
    
    def test_road_condition_property(self):
        """
        Test road_condition property
        """
        test_value = 'ztzajzncfrperjkezskg'
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
        test_value = 'ntekairzeffcokzhzity'
        self.instance.restriction_one_direction = test_value
        self.assertEqual(self.instance.restriction_one_direction, test_value)
    
    def test_restriction_one_text_property(self):
        """
        Test restriction_one_text property
        """
        test_value = 'tolpofedkwynzowvbunw'
        self.instance.restriction_one_text = test_value
        self.assertEqual(self.instance.restriction_one_text, test_value)
    
    def test_restriction_two_direction_property(self):
        """
        Test restriction_two_direction property
        """
        test_value = 'euplfauqictbijlleqxo'
        self.instance.restriction_two_direction = test_value
        self.assertEqual(self.instance.restriction_two_direction, test_value)
    
    def test_restriction_two_text_property(self):
        """
        Test restriction_two_text property
        """
        test_value = 'oaxgrjtrsokrgzfocqvi'
        self.instance.restriction_two_text = test_value
        self.assertEqual(self.instance.restriction_two_text, test_value)
    
    def test_date_updated_property(self):
        """
        Test date_updated property
        """
        test_value = 'nfaulagnjgtqxtiabtck'
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

