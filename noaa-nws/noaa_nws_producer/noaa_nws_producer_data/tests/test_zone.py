"""
Test case for Zone
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_nws_producer_data.zone import Zone


class Test_Zone(unittest.TestCase):
    """
    Test case for Zone
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Zone.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Zone for testing
        """
        instance = Zone(
            zone_id='yygrkejxwuhgonilplva',
            name='qdajloadgqeumloglnca',
            type='fdtrgkgihzrqxiuzrnyp',
            state='txbhqzpjtcmkmnhavhsq',
            forecast_office='rcfjittcwbowmjekftik',
            timezone='cuzdcgjvhocenkzmhxeq',
            radar_station='gzzwxcmfsxakiefoqnwm'
        )
        return instance

    
    def test_zone_id_property(self):
        """
        Test zone_id property
        """
        test_value = 'yygrkejxwuhgonilplva'
        self.instance.zone_id = test_value
        self.assertEqual(self.instance.zone_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'qdajloadgqeumloglnca'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'fdtrgkgihzrqxiuzrnyp'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'txbhqzpjtcmkmnhavhsq'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_forecast_office_property(self):
        """
        Test forecast_office property
        """
        test_value = 'rcfjittcwbowmjekftik'
        self.instance.forecast_office = test_value
        self.assertEqual(self.instance.forecast_office, test_value)
    
    def test_timezone_property(self):
        """
        Test timezone property
        """
        test_value = 'cuzdcgjvhocenkzmhxeq'
        self.instance.timezone = test_value
        self.assertEqual(self.instance.timezone, test_value)
    
    def test_radar_station_property(self):
        """
        Test radar_station property
        """
        test_value = 'gzzwxcmfsxakiefoqnwm'
        self.instance.radar_station = test_value
        self.assertEqual(self.instance.radar_station, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Zone.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Zone.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

